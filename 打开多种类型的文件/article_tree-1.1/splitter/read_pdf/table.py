from pdfplumber import utils
from operator import itemgetter
import itertools

DEFAULT_SNAP_TOLERANCE = 3
DEFAULT_JOIN_TOLERANCE = 3
DEFAULT_MIN_WORDS_VERTICAL = 3
DEFAULT_MIN_WORDS_HORIZONTAL = 1


def move_to_avg(objs, orientation):
    """
    Move `objs` vertically/horizontally to their average x/y position.
    """
    if orientation not in ("h", "v"):
        raise ValueError("Orientation must be 'v' or 'h'")
    if len(objs) == 0:
        return []
    move_axis = "v" if orientation == "h" else "h"
    attr = "top" if orientation == "h" else "x0"
    values = list(map(itemgetter(attr), objs))
    q = pow(10, utils.decimalize(values[0]).as_tuple().exponent)
    avg = utils.decimalize(float(sum(values) / len(values)), q)
    new_objs = [utils.move_object(obj, move_axis, avg - obj[attr])
                for obj in objs]
    return new_objs


def snap_edges(edges, tolerance=DEFAULT_SNAP_TOLERANCE):
    """
    Given a list of edges, snap any within `tolerance` pixels of one another to their positional average.
    """
    v, h = [list(filter(lambda x: x["orientation"] == o, edges)) for o in ("v", "h")]

    v = [move_to_avg(cluster, "v") for cluster in utils.cluster_objects(v, "x0", tolerance)]

    h = [move_to_avg(cluster, "h") for cluster in utils.cluster_objects(h, "top", tolerance)]

    snapped = list(itertools.chain(*(v + h)))
    return snapped


def join_edge_group(edges, orientation, tolerance=DEFAULT_JOIN_TOLERANCE):
    """
    Given a list of edges along the same infinite line, join those that are within `tolerance` pixels of one another.
    """
    if orientation == "h":
        min_prop, max_prop = "x0", "x1"
    elif orientation == "v":
        min_prop, max_prop = "top", "bottom"
    else:
        raise ValueError("Orientation must be 'v' or 'h'")

    sorted_edges = list(sorted(edges, key=itemgetter(min_prop)))
    joined = [sorted_edges[0]]
    for e in sorted_edges[1:]:
        last = joined[-1]
        if e[min_prop] <= (last[max_prop] + tolerance):
            if e[max_prop] > last[max_prop]:
                # Extend current edge to new extremity
                joined[-1] = utils.resize_object(last, max_prop, e[max_prop])
            else:
                # Do nothing; edge is fully contained in pre-existing edge
                pass
        else:
            # Edge is separate from previous edges
            joined.append(e)

    return joined


def merge_edges(edges, snap_tolerance, join_tolerance):
    """
    Using the `snap_edges` and `join_edge_group` methods above, merge a list of edges into a more "seamless" list.
    """
    def get_group(edge):
        if edge["orientation"] == "h":
            return "h", edge["top"]
        else:
            return "v", edge["x0"]

    if snap_tolerance > 0:
        edges = snap_edges(edges, snap_tolerance)

    if join_tolerance > 0:
        _sorted = sorted(edges, key=get_group)
        edge_groups = itertools.groupby(_sorted, key=get_group)
        edge_gen = (join_edge_group(items, k[0], join_tolerance)
                    for k, items in edge_groups)
        edges = list(itertools.chain(*edge_gen))
    return edges


def words_to_edges_h(words, word_threshold=DEFAULT_MIN_WORDS_HORIZONTAL):
    """
    Find (imaginary) horizontal lines that connect the tops of at least `word_threshold` words.
    """
    by_top = utils.cluster_objects(words, "top", 1)
    large_clusters = filter(lambda x: len(x) >= word_threshold, by_top)
    rects = list(map(utils.objects_to_rect, large_clusters))
    if len(rects) == 0:
        return []
    min_x0 = min(map(itemgetter("x0"), rects))
    max_x1 = max(map(itemgetter("x1"), rects))
    edges = [{
        "x0": min_x0,
        "x1": max_x1,
        "top": r["top"],
        "bottom": r["top"],
        "width": max_x1 - min_x0,
        "orientation": "h"
    } for r in rects] + [{
        "x0": min_x0,
        "x1": max_x1,
        "top": r["bottom"],
        "bottom": r["bottom"],
        "width": max_x1 - min_x0,
        "orientation": "h"
    } for r in rects]

    return edges


def words_to_edges_v(words, word_threshold=DEFAULT_MIN_WORDS_VERTICAL):
    """
    Find (imaginary) vertical lines that connect the left, right, or center of at least `word_threshold` words.
    """
    # Find words that share the same left, right, or centerpoints
    by_x0 = utils.cluster_objects(words, "x0", word_threshold)  # 左对齐
    by_x1 = utils.cluster_objects(words, "x1", word_threshold)  # 右对齐
    by_center = utils.cluster_objects(words, lambda x: (x["x0"] + x["x1"])/2, word_threshold)  # 居中对齐
    clusters = by_x0 + by_x1 + by_center

    # Find the points that align with the most words
    sorted_clusters = sorted(clusters, key=lambda x: -len(x))
    large_clusters = filter(lambda x: len(x) >= word_threshold, sorted_clusters)

    # For each of those points, find the rectangles fitting all matching words
    rects = list(map(utils.objects_to_rect, large_clusters))

    # Iterate through those rectangles, condensing overlapping rectangles
    condensed_rects = []
    for rect in rects:
        overlap = False
        for c in condensed_rects:
            if utils.objects_overlap(rect, c):
                overlap = True
                break
        if overlap is False:
            condensed_rects.append(rect)

    if len(condensed_rects) == 0:
        return []
    sorted_rects = list(sorted(condensed_rects, key=itemgetter("x0")))

    # Find the far-right boundary of the rightmost rectangle
    last_rect = sorted_rects[-1]
    while True:
        words_inside = utils.intersects_bbox(
            [w for w in words if w["x0"] >= last_rect["x0"]],
            (last_rect["x0"], last_rect["top"], last_rect["x1"], last_rect["bottom"]),
        )
        rect = utils.objects_to_rect(words_inside)
        if rect == last_rect:
            break
        else:
            last_rect = rect

    # Describe all the left-hand edges of each text cluster
    edges = [{
        "x0": b["x0"],
        "x1": b["x0"],
        "top": b["top"],
        "bottom": b["bottom"],
        "height": b["bottom"] - b["top"],
        "orientation": "v"
    } for b in sorted_rects] + [{
        "x0": last_rect["x1"],
        "x1": last_rect["x1"],
        "top": last_rect["top"],
        "bottom": last_rect["bottom"],
        "height": last_rect["bottom"] - last_rect["top"],
        "orientation": "v"
    }]

    return edges


def set_columns(word, top, bottom):
    """此时求出的是单词盒子，因此暂时不加线宽和线条分类"""
    return {
        "x0": word['x0'],
        "x1": word['x1'],
        "top": top,
        "bottom": bottom,
        # "width": 1,
        # "orientation": "v",
    }


def merger(lines):
    """同行合并：合并同行表格的多行内容"""
    for line in lines:
        top, bottom = line[0]
        words = line[1]
        if words == list():
            continue
        columns = [set_columns(words[0], top['top'], bottom['bottom'])]
        for word in words[1:]:
            in_column = False
            for column in columns:
                if not (word['x0'] >= column['x1'] or word['x1'] <= column['x0']):
                    column['x0'] = min(word['x0'], column['x0'])
                    column['x1'] = max(word['x1'], column['x1'])
                    in_column = True
            if not in_column:
                columns.append(set_columns(word, top['top'], bottom['bottom']))
        line[1] = columns
    return lines


def set_column(column, x0, top, x1, bottom, *args, **kwargs):
    column = column.copy()
    column['x0'] = min(x0, column['x0'])
    column['top'] = min(top, column['top'])
    column['x1'] = max(x1, column['x1'])
    column['bottom'] = max(bottom, column['bottom'])
    return column


def with_columns(
        lines,
        word_threshold=DEFAULT_MIN_WORDS_HORIZONTAL,
):
    """同列合并：合并表格的中的列"""
    lines = lines.copy()
    tables = [[]]
    for line in lines:
        words = line[1]
        for word in words:
            # 如果是表中的首行，直接添加到表中
            if tables[-1] == list():
                # 此处应该先判断该行是否为表格行，再考虑是否加入表格
                # 由于有些文章有页眉，因此很容易将第一段认定为表格行
                # 目前暂不添加

                # 初始化columns目前每个column拥有四个参数x0, x1, top, bottom
                columns = list(map(lambda x: x.copy(), line[1]))
                tables[-1] = columns
                continue
            # 如果在首列之前，直接在首位添加一个列
            if word['x1'] < tables[-1][0]['x0']:
                tables[-1] = [word] + tables[-1]
                continue
            # 如果在尾列之后，直接在尾位添加一个列
            if word['x0'] > tables[-1][-1]['x1']:
                tables[-1] = tables[-1] + [word]
                continue
            # # 否则在表中添加一个新点，无序
            # tables[-1].append(set_columns(word, top['top'], bottom['bottom']))
            for n, column in enumerate(tables[-1], 0):
                # 在列中，且在两列之间的，在对应位置添加列
                if n != 0 and n != len(tables[-1]) - 1:
                    if word['x0'] >= column['x1'] and word['x1'] <= tables[-1][n - 1]['x0']:
                        tables[-1] = tables[-1][:n] + [word] + tables[-1][n:]
                        break
                # 如果该词与当前列有交叉，更新当前列
                is_cross = False  # 是否与前/后列有交叉
                if not (word['x0'] >= column['x1'] or word['x1'] <= column['x0']):
                    # 如果超出当前列到左侧列，合并两列，合并后再与再之前的列判断
                    while n > 0 and word['x0'] < tables[-1][n - 1]['x1']:
                        is_cross = True
                        if len(words) == 1:  # 认为是正常文本并非表格, 建立新表
                            tables.append([])
                            break
                        # 合并单元格
                        column = set_column(column, tables[-1][n - 1]['x0'],
                                            word['top'], word['x1'], word['bottom'])
                        tables[-1][n] = column
                        tables[-1].pop(n - 1)
                        n -= 1  # 前一个被删除后，该词即为前一个词
                    # 如果超出当前列到右侧列，合并两列，合并后再与再之前的列判断
                    while n < len(tables[-1]) - 1 and word['x1'] > tables[-1][n + 1]['x0']:
                        is_cross = True
                        if len(words) == 1:  # 认为是正常文本并非表格, 建立新表
                            tables.append([])
                            break
                        # 合并单元格
                        column['x0'] = min(column['x0'], word['x0'])
                        column['x1'] = max(tables[-1][n + 1]['x1'], word['x1'])
                        tables[-1][n] = column
                        tables[-1].pop(n + 1)
                        # right_n += 1  # 即使后一个词被删除也不影响当前词的位置
                    # 因为有可能即与左边又与右边有交叉
                    if is_cross:
                        break
                    else:
                        # 未超出当前列
                        tables[-1][n] = set_column(column, **word)
                        # 在未超出当前列时，还存在存在表头的情况，即上一行的某列对应之后的多列
                        # 该情况应设置多级列标识，但目前先不添加此功能
                        break

    # 过滤掉行数不足的“表”
    tables_filter = filter(lambda x: len(x) >= word_threshold, tables)
    return tables_filter


def set_v(x, top, bottom):
    return {
        "x0": x,
        "x1": x,
        "top": top,
        "bottom": bottom,
        "height": bottom - top,
        "orientation": "v",
    }


def get_bbox(table):
    return (
        min(map(lambda x: x['x0'], table)),
        min(map(lambda x: x['top'], table)),
        max(map(lambda x: x['x1'], table)),
        max(map(lambda x: x['bottom'], table))
    )


def columns2v(tables, word_threshold=DEFAULT_MIN_WORDS_VERTICAL):
    """取两列的中线作为表格的竖线，并在表格两头加上封口的竖线"""
    v = []
    for table in tables:
        if len(table) < word_threshold:
            # 超过word_threshold行才算表格
            continue
        x0, top, x1, bottom = get_bbox(table)
        v.append(set_v(x0, top, bottom))
        for before, after in zip(table[:-1], table[1:]):
            x = (before['x1'] + after['x0']) / 2
            # print(before['top'], after['top'], before['bottom'], after['bottom'])
            min_top = min(before['top'], after['top'])
            max_bottom = max(before['bottom'], after['bottom'])
            v.append(set_v(x, min_top, max_bottom))
        v.append(set_v(x1, top, bottom))
    return v


def words_to_edges_v2(
        words, h,
        words_horizontal=DEFAULT_MIN_WORDS_HORIZONTAL,
        words_vertical=DEFAULT_MIN_WORDS_VERTICAL,
):
    if len(h) < 3:  # 横线少于三根认为不是表
        return []
    by_top = utils.cluster_objects(words, "top", 1)  # 确定同行词
    lines = []
    for top, bottom in zip(h[:-1], h[1:]):
        lines.append([(top, bottom), []])
        for words in by_top:
            if top['top'] <= (words[0]['top']+words[0]['bottom'])/2 <= bottom['bottom']:
                lines[-1][1].extend(words)
    lines = merger(lines)  # 将有回车换行的的内容合并到同行，避免词太零散
    # 将同列的词框入同框，同时区分有多少个表
    # 单行只有一个字段，且横跨多行时认为是普通文本
    columns = with_columns(lines, words_horizontal)
    # 根据画框绘制表分割竖线
    v = columns2v(columns, words_vertical)
    return v


def edges_to_intersections(edges, x_tolerance=1, y_tolerance=1):
    """
    Given a list of edges, return the points at which they intersect within `tolerance` pixels.
    """
    intersections = {}
    v_edges, h_edges = [list(filter(lambda x: x["orientation"] == o, edges)) for o in ("v", "h")]
    for v in sorted(v_edges, key=itemgetter("x0", "top")):
        for h in sorted(h_edges, key=itemgetter("top", "x0")):
            if ((v["top"] <= (h["top"] + y_tolerance)) and
                    (v["bottom"] >= (h["top"] - y_tolerance)) and
                    (v["x0"] >= (h["x0"] - x_tolerance)) and
                    (v["x0"] <= (h["x1"] + x_tolerance))):
                vertex = (v["x0"], h["top"])
                if vertex not in intersections:
                    intersections[vertex] = {"v": [], "h": []}
                intersections[vertex]["v"].append(v)
                intersections[vertex]["h"].append(h)
    return intersections


def intersections_to_cells(intersections):
    """
    Given a list of points (`intersections`), return all retangular "cells" those points describe.

    `intersections` should be a dictionary with (x0, top) tuples as keys,
    and a list of edge objects as values. The edge objects should correspond
    to the edges that touch the intersection.
    """

    def edge_connects(p1, p2):
        def edges_to_set(edges):
            return set(map(utils.obj_to_bbox, edges))

        if p1[0] == p2[0]:
            common = edges_to_set(intersections[p1]["v"]) \
                .intersection(edges_to_set(intersections[p2]["v"]))
            if len(common):
                return True

        if p1[1] == p2[1]:
            common = edges_to_set(intersections[p1]["h"]) \
                .intersection(edges_to_set(intersections[p2]["h"]))
            if len(common):
                return True
        return False

    points = list(sorted(intersections.keys()))
    n_points = len(points)

    def find_smallest_cell(points, i):
        if i == n_points - 1:
            return None
        pt = points[i]
        rest = points[i+1:]
        # Get all the points directly below and directly right
        below = [x for x in rest if x[0] == pt[0]]
        right = [x for x in rest if x[1] == pt[1]]
        for below_pt in below:
            if not edge_connects(pt, below_pt):
                continue

            for right_pt in right:
                if not edge_connects(pt, right_pt):
                    continue

                bottom_right = (right_pt[0], below_pt[1])

                if ((bottom_right in intersections) and
                        edge_connects(bottom_right, right_pt) and
                        edge_connects(bottom_right, below_pt)):

                    return (
                        pt[0],
                        pt[1],
                        bottom_right[0],
                        bottom_right[1]
                    )

    cell_gen = (find_smallest_cell(points, i) for i in range(len(points)))
    return list(filter(None, cell_gen))


def cells_to_tables(cells):
    """
    Given a list of bounding boxes (`cells`), return a list of tables that hold those
    those cells most simply (and contiguously).
    """
    def bbox_to_corners(bbox):
        x0, top, x1, bottom = bbox
        return list(itertools.product((x0, x1), (top, bottom)))

    cells = [{
        "available": True,
        "bbox": bbox,
        "corners": bbox_to_corners(bbox)
    } for bbox in cells]

    # Iterate through the cells found above, and assign them
    # to contiguous tables

    def init_new_table():
        return {"corners": set([]), "cells": []}

    def assign_cell(cell, table):
        table["corners"] = table["corners"].union(set(cell["corners"]))
        table["cells"].append(cell["bbox"])
        cell["available"] = False

    n_cells = len(cells)
    n_assigned = 0
    tables = []
    current_table = init_new_table()
    while True:
        initial_cell_count = len(current_table["cells"])
        for i, cell in enumerate(filter(itemgetter("available"), cells)):
            if len(current_table["cells"]) == 0:
                assign_cell(cell, current_table)
                n_assigned += 1
            else:
                corner_count = sum(c in current_table["corners"]
                                   for c in cell["corners"])
                if corner_count > 0 and cell["available"]:
                    assign_cell(cell, current_table)
                    n_assigned += 1
        if n_assigned == n_cells:
            break
        if len(current_table["cells"]) == initial_cell_count:
            tables.append(current_table)
            current_table = init_new_table()

    if len(current_table["cells"]):
        tables.append(current_table)

    _sorted = sorted(tables, key=lambda t: min(t["corners"]))
    filtered = [t["cells"] for t in _sorted if len(t["cells"]) > 1]
    return filtered


class CellGroup(object):
    def __init__(self, cells):
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), filter(None, cells))),
            min(map(itemgetter(1), filter(None, cells))),
            max(map(itemgetter(2), filter(None, cells))),
            max(map(itemgetter(3), filter(None, cells))),
        )


class Row(CellGroup):
    pass


class Table(object):
    def __init__(self, page, cells):
        self.page = page
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), cells)),
            min(map(itemgetter(1), cells)),
            max(map(itemgetter(2), cells)),
            max(map(itemgetter(3), cells)),
        )

    @property
    def rows(self):
        _sorted = sorted(self.cells, key=itemgetter(1, 0))
        xs = list(sorted(set(map(itemgetter(0), self.cells))))
        rows = []
        for y, row_cells in itertools.groupby(_sorted, itemgetter(1)):
            xdict = dict((cell[0], cell) for cell in row_cells)
            row = Row([xdict.get(x) for x in xs])
            rows.append(row)
        return rows

    def extract(self,
                x_tolerance=utils.DEFAULT_X_TOLERANCE,
                y_tolerance=utils.DEFAULT_Y_TOLERANCE):

        chars = self.page.chars
        table_arr = []

        def char_in_bbox(char, bbox):
            v_mid = (char["top"] + char["bottom"]) / 2
            h_mid = (char["x0"] + char["x1"]) / 2
            x0, top, x1, bottom = bbox
            return (
                    (h_mid >= x0) and
                    (h_mid < x1) and
                    (v_mid >= top) and
                    (v_mid < bottom)
            )

        for row in self.rows:
            arr = []
            row_chars = [char for char in chars if char_in_bbox(char, row.bbox)]

            for cell in row.cells:
                if cell is None:
                    cell_text = None
                else:
                    cell_chars = [char for char in row_chars if char_in_bbox(char, cell)]

                    if len(cell_chars):
                        cell_text = utils.extract_text(cell_chars,
                                                       x_tolerance=x_tolerance,
                                                       y_tolerance=y_tolerance).strip()
                    else:
                        cell_text = ""
                arr.append(cell_text)
            table_arr.append(arr)

        return table_arr


TABLE_STRATEGIES = ["lines", "lines_strict", "text", "explicit", "text2", "auto"]
DEFAULT_TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [],
    "explicit_horizontal_lines": [],
    "snap_tolerance": DEFAULT_SNAP_TOLERANCE,
    "join_tolerance": DEFAULT_JOIN_TOLERANCE,
    "edge_min_length": 3,
    "min_words_vertical": DEFAULT_MIN_WORDS_VERTICAL,
    "min_words_horizontal": DEFAULT_MIN_WORDS_HORIZONTAL,
    "keep_blank_chars": False,
    "text_tolerance": 3,
    "text_x_tolerance": None,
    "text_y_tolerance": None,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": None,
    "intersection_y_tolerance": None,
    "lines_min_quantity": 3,  # 在outo时使用，线的数量的最小值
    "lines_min_h_quantity": None,
    "lines_min_v_quantity": None,
    # "auto_not_double_text": True,  # 不允许横纵线都为文字对齐方式获取
}


class TableFinder(object):
    """
    Given a PDF page, find plausible table structures.

    Largely borrowed from Anssi Nurminen's master's thesis: http://dspace.cc.tut.fi/dpub/bitstream/handle/123456789/21520/Nurminen.pdf?sequence=3

    ... and inspired by Tabula: https://github.com/tabulapdf/tabula-extractor/issues/16
    """
    def __init__(self, page, settings={}):
        for k in settings.keys():
            if k not in DEFAULT_TABLE_SETTINGS:
                raise ValueError("Unrecognized table setting: '{0}'".format(
                    k
                ))
        self.page = page
        self.settings = dict(DEFAULT_TABLE_SETTINGS)
        self.settings.update(settings)
        for var, fallback in [
            ("text_x_tolerance", "text_tolerance"),
            ("text_y_tolerance", "text_tolerance"),
            ("intersection_x_tolerance", "intersection_tolerance"),
            ("intersection_y_tolerance", "intersection_tolerance"),
            ("lines_min_h_quantity", "lines_min_quantity"),
            ("lines_min_v_quantity", "lines_min_quantity"),
        ]:
            if self.settings[var] is None:
                self.settings.update({
                    var: self.settings[fallback]
                })
        self.edges = None
        self.intersections = None
        self.cells = None
        self.tables = None

    def find_table(self):
        edges = self.get_edges()  # 获取边界
        return self._find_table(edges)

    def _find_table(self, edges=None):
        self.edges = edges
        self.intersections = edges_to_intersections(
            self.edges,
            self.settings["intersection_x_tolerance"],
            self.settings["intersection_y_tolerance"],
        )  # 获取表格交叉点
        self.cells = intersections_to_cells(
            self.intersections
        )  # 获取单元格
        self.tables = [Table(self.page, t) for t in cells_to_tables(self.cells)]  # 获取单元格数据
        return self

    def get_edges(self):
        v_strat, h_strat, words = self.set_v_h_strat()
        h, h_strat = self._get_h(h_strat, words=words)
        v, v_strat = self._get_v(v_strat, words=words, h=h)
        return list(v) + list(h)

    def get_v(self):
        v_strat, h_strat, words = self.set_v_h_strat()
        return self._get_v(v_strat, words=words)

    def get_h(self):
        v_strat, h_strat, words = self.set_v_h_strat()
        return self._get_h(h_strat, words=words)

    def set_v_h_strat(self):
        settings = self.settings
        for name in ["vertical", "horizontal"]:
            strategy = settings[name + "_strategy"]
            if strategy not in TABLE_STRATEGIES:
                raise ValueError("{0} must be one of {{{1}}}".format(
                    name + "_strategy",
                    ",".join(TABLE_STRATEGIES)
                ))
            if strategy == "explicit":
                if len(settings["explicit_" + name + "_lines"]) < 2:
                    raise ValueError("If {0} == 'explicit', {1} must be specified as list/tuple of two "
                                     "or more floats/ints.".format(strategy + "_strategy",
                                                                   "explicit_" + name + "_lines", ))

        v_strat = settings["vertical_strategy"]
        h_strat = settings["horizontal_strategy"]
        return v_strat, h_strat, self.get_words(v_strat, h_strat)

    def get_words(self, v_strat, h_strat):
        words = None
        if v_strat in ["text", "text2", 'auto'] or h_strat in ["text", "auto"]:
            xt = self.settings["text_x_tolerance"]
            if xt is None:
                xt = self.settings["text_tolerance"]
            yt = self.settings["text_y_tolerance"]
            if yt is None:
                yt = self.settings["text_tolerance"]
            words = self.page.extract_words(
                x_tolerance=xt,
                y_tolerance=yt,
                keep_blank_chars=self.settings["keep_blank_chars"]
            )
        return words

    def _get_v(self, v_strat, words=None, h=None):

        def v_edge_desc_to_edge(desc):
            if isinstance(desc, dict):
                edge = {
                    "x0": desc.get("x0", desc.get("x")),
                    "x1": desc.get("x1", desc.get("x")),
                    "top": desc.get("top", self.page.bbox[1]),
                    "bottom": desc.get("bottom", self.page.bbox[3]),
                    "orientation": "v"
                }
            else:
                edge = {
                    "x0": desc,
                    "x1": desc,
                    "top": self.page.bbox[1],
                    "bottom": self.page.bbox[3],
                }
            edge["height"] = edge["bottom"] - edge["top"]
            edge["orientation"] = "v"
            return edge

        v_explicit = list(map(v_edge_desc_to_edge, self.settings["explicit_vertical_lines"]))

        if v_strat == "lines":
            v_base = utils.filter_edges(self.page.edges, "v")
        elif v_strat == "lines_strict":
            v_base = utils.filter_edges(self.page.edges, "v",
                                        edge_type="lines")
        elif v_strat == "text":  # 该方式效果不佳，已舍弃
            v_base = words_to_edges_v(words, word_threshold=self.settings["min_words_vertical"])
        elif v_strat == "text2":  # 词在同一列认为是同列的，扩散到其他列则将两列内容合并
            v_base = words_to_edges_v2(
                words, h,
                words_horizontal=self.settings["min_words_horizontal"],
                words_vertical=self.settings["min_words_vertical"])
        elif v_strat == "explicit":
            v_base = []
        elif v_strat == "auto":
            result = self._get_v("lines", words, h)  # 先按线的方式获取
            # 线的数量至少要有（默认3）条
            if len(result[0]) >= self.settings["lines_min_v_quantity"]:
                return result
            # 否则采用文本对齐的方式获取
            else:
                return self._get_v("text2", words, h)
        else:
            raise ValueError("未知的v_strat，应在以下结果中选择：lines, lines_strict, text, explicit, text2, auto")

        v = v_base + v_explicit
        if self.settings["snap_tolerance"] > 0 or self.settings["join_tolerance"] > 0:
            v = merge_edges(v,
                            snap_tolerance=self.settings["snap_tolerance"],
                            join_tolerance=self.settings["join_tolerance"],
                            )
        return utils.filter_edges(v, min_length=self.settings["edge_min_length"]), v_strat

    def _get_h(self, h_strat, words=None):

        def h_edge_desc_to_edge(desc):
            if isinstance(desc, dict):
                edge = {
                    "x0": desc.get("x0", self.page.bbox[0]),
                    "x1": desc.get("x1", self.page.bbox[2]),
                    "top": desc.get("top", desc.get("bottom")),
                    "bottom": desc.get("bottom", desc.get("top")),
                }
            else:
                edge = {
                    "x0": self.page.bbox[0],
                    "x1": self.page.bbox[2],
                    "top": desc,
                    "bottom": desc,
                }
            edge["width"] = edge["x1"] - edge["x0"]
            edge["orientation"] = "h"
            return edge

        h_explicit = list(map(h_edge_desc_to_edge, self.settings["explicit_horizontal_lines"]))

        if h_strat == "lines":
            h_base = utils.filter_edges(self.page.edges, "h")
        elif h_strat == "lines_strict":
            h_base = utils.filter_edges(self.page.edges, "h",
                                        edge_type="lines")
        elif h_strat == "text":
            h_base = words_to_edges_h(words,
                                      word_threshold=self.settings["min_words_horizontal"])
        elif h_strat == "explicit":
            h_base = []
        elif h_strat == "auto":
            result = self._get_h("lines", words)
            if len(result[0]) >= self.settings["lines_min_h_quantity"]:
                return result
            else:
                return self._get_h("text", words)
        else:
            raise ValueError("未知的h_strat，应在以下结果中选择：lines, lines_strict, text, explicit, auto")

        h = h_base + h_explicit

        if self.settings["snap_tolerance"] > 0 or self.settings["join_tolerance"] > 0:
            h = merge_edges(h,
                            snap_tolerance=self.settings["snap_tolerance"],
                            join_tolerance=self.settings["join_tolerance"],
                            )
        return utils.filter_edges(h, min_length=self.settings["edge_min_length"]), h_strat
