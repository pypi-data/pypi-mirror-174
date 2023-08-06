#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from collections import namedtuple


def psdParseDecoder(psdParseDict):
    return namedtuple('PsdParseInfo', psdParseDict.keys())(*psdParseDict.values())


class PsdParseInfo(object):

    def __init__(self):
        self.file_path = ''
        self.frame_width = 0
        self.frame_height = 0
        self.main_img_path = ''
        self.main_img_width = 0
        self.main_img_height = 0
        self.main_border_color = ''
        self.main_border_gradient_coordinates = []
        self.main_border_gradient_colors = []
        self.main_border_text = ''
        self.main_border_logo_path = ''
        self.main_border_logo_width = 0
        self.main_border_logo_height = 0
        self.camera_border_color = ''
        self.camera_border_gradient_coordinates = []
        self.camera_border_gradient_colors = []
        self.camera_border_text = ''
        self.camera_border_logo_path = ''
        self.camera_border_logo_width = 0
        self.camera_border_logo_height = 0
        self.camera_lens_colors = []

    def __str__(self):
        return self.__class__.__name__ + '(' + ', '.join(['%s: %s' % item for item in self.__dict__.items()]) + ')'

    @staticmethod
    def fromJson(json_str: str):
        return json.loads(json_str,  object_hook=psdParseDecoder)


if __name__ == '__main__':
    info = PsdParseInfo()
    print(info)
    info = PsdParseInfo.fromJson(json.dumps(info.__dict__))
