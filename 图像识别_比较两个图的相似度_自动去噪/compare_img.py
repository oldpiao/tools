# Filename: histsimilar.py
# -*- coding: utf-8 -*-

from PIL import Image


def make_regalur_image(img, size=(256, 256)):
    return img.resize(size).convert('RGB')


def split_image(img, part_size=(64, 64)):
    w, h = img.size
    pw, ph = part_size

    assert w % pw == h % ph == 0

    return [img.crop((i, j, i + pw, j + ph)).copy() for i in range(0, w, pw) for j in range(0, h, ph)]


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


def calc_similar(li, ri):
    #   return hist_similar(li.histogram(), ri.histogram())
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


def calc_similar_by_path(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    return calc_similar(li, ri)


def make_doc_data(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    li.save(lf + '_regalur.png')
    ri.save(rf + '_regalur.png')
    fd = open('stat.csv', 'w')
    fd.write('\n'.join(l + ',' + r for l, r in zip(map(str, li.histogram()), map(str, ri.histogram()))))
    #   print >>fd, '\n'
    #   fd.write(','.join(map(str, ri.histogram())))
    fd.close()
    from PIL import ImageDraw
    li = li.convert('RGB')
    draw = ImageDraw.Draw(li)
    for i in range(0, 256, 64):
        draw.line((0, i, 256, i), fill='#ff0000')
        draw.line((i, 0, i, 256), fill='#ff0000')
    li.save(lf + '_lines.png')


if __name__ == '__main__':
    similarity = calc_similar_by_path('img_all/000_bg.png', 'img_all/001_bg.png') * 100
    print(similarity)
    # for i in range(50):
    #     # similarity = calc_similar_by_path('img2/001_bg.png', 'img2/%s_bg.png' % ('0'*(3-len(str(i)))+str(i))) * 100
    #     similarity = calc_similar_by_path(open('img_all/001_bg.png', 'rb'), open('img2/%s_bg.png' % ('0'*(3-len(str(i)))+str(i)), 'rb')) * 100
    #     if similarity > 85:
    #         print(similarity, i)


#   make_doc_data('test/TEST4/1.JPG', 'test/TEST4/2.JPG')