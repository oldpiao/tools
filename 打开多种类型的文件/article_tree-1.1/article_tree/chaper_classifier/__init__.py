# -*- coding: utf-8 -*-

from article_tree.chaper_classifier.judge_chaper import *
from article_tree.chaper_classifier.proxy import ChaperClassifier


def chaper_classifier(string):
    cc = ChaperClassifier()
    cc.init(string)
    cc.verify_and_cut_st()
    return cc
