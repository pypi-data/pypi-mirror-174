#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2 as cv
from PsdParser import PsdParser
from Compounder import ImgCompounder


def run():
    psd_parser = PsdParser(psd_file_path='/Users/patrick/PycharmProjects/pylion/aaa2210210007.psd',
                           parse_img_dic_path='/Users/patrick/Downloads/ex_lion/res/img/parse')
    psd_parse_info = psd_parser.parse()
    print('[*] psd 解析结果: %s' % psd_parse_info.__str__())
    compounder = ImgCompounder(psd_parse_info=psd_parse_info,
                               template=None,
                               history_id='test',
                               compound_img_dir_path='/Users/patrick/Downloads/ex_lion/res/img/compound',
                               compound_img_dir_url='http://localhost:8018/ex_lion/res/img/compound',
                               font_path='/Users/patrick/PycharmProjects/ex_lion/fonts/Arial-Bold.ttf')
    compound_result = compounder.draw()
    print('[*] 图片合成结果: %s' % compound_result.__str__())


if __name__ == '__main__':
    run()
