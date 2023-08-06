#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from PIL import Image
from psd_tools import PSDImage
from psd_tools.constants import ColorMode
from . import logger
from .PsdParseInfo import PsdParseInfo


def rgb_to_hex(rgba: tuple):
    color = '#'
    color += str(hex(rgba[0]))[-2:].replace('x', '0').upper()
    color += str(hex(rgba[1]))[-2:].replace('x', '0').upper()
    color += str(hex(rgba[2]))[-2:].replace('x', '0').upper()
    return color


class PsdParser:

    def __init__(self, psd_file_path: str, parse_img_dic_path: str):
        self.file_path = psd_file_path
        self.parse_img_dic_path = parse_img_dic_path
        assert os.path.exists(self.file_path), '需要解析的文件路径不存在'
        assert self.file_path.endswith('.psd'), '要解析的文件格式错误'
        self.file_name = self.file_path.split('/')[-1].split(".")[0]
        assert self.file_name and len(self.file_name) > 0, '文件名称获取失败'
        self.psd = PSDImage.open(self.file_path)
        assert self.psd.color_mode == ColorMode.RGB, 'psd文件的颜色模式错误: %s' % self.psd.color_mode
        self.frame_width = self.psd.size[0]
        self.frame_height = self.psd.size[1]
        self.psd_parse_info = PsdParseInfo()
        self.psd_parse_info.file_path = psd_file_path
        self.psd_parse_info.frame_width = self.frame_width
        self.psd_parse_info.frame_height = self.frame_height

    def parse(self):
        logger.info('[*] 开始解析PSD文件: %s' % self.file_path)
        logger.info('[*] ')
        for layer in self.psd:
            if layer.width <= 0 or layer.height <= 0:
                continue
            if layer.name == 'main_img':
                self.__parse_main_img(layer)
            elif layer.name == 'main_border':
                self.__parse_main_border(layer)
            elif layer.name == 'main_border_gradient':
                self.__parse_main_border_gradient(layer)
            elif layer.name == 'main_border_gradient_coordinate':
                self.__parse_main_border_gradient_coordinate(layer)
            elif layer.name == 'main_border_text':
                self.__parse_main_border_text(layer)
            elif layer.name == 'main_border_logo':
                self.__parse_main_border_logo(layer)
            elif layer.name == 'camera_border':
                self.__parse_camera_border(layer)
            elif layer.name == 'camera_border_gradient':
                self.__parse_camera_border_gradient(layer)
            elif layer.name == 'camera_border_gradient_coordinate':
                self.__parse_camera_border_gradient_coordinate(layer)
            elif layer.name == 'camera_border_text':
                self.__parse_camera_border_text(layer)
            elif layer.name == 'camera_border_logo':
                self.__parse_camera_border_logo(layer)
            elif layer.name == 'camera_lens1':
                camera_lens_color = self.__parse_camera_lens(layer)
                self.psd_parse_info.camera_lens_colors.append(camera_lens_color)
            elif layer.name == 'camera_lens2':
                camera_lens_color = self.__parse_camera_lens(layer)
                self.psd_parse_info.camera_lens_colors.append(camera_lens_color)
            elif layer.name == 'camera_lens3':
                camera_lens_color = self.__parse_camera_lens(layer)
                self.psd_parse_info.camera_lens_colors.append(camera_lens_color)
            elif layer.name == 'camera_lens4':
                camera_lens_color = self.__parse_camera_lens(layer)
                self.psd_parse_info.camera_lens_colors.append(camera_lens_color)

        return self.psd_parse_info

    def __parse_main_img(self, layer):
        try:
            if layer.kind != 'pixel':
                logger.error('[*] 主图图层类型错误')
                return
            logger.info("[*] 主图层开始解析")
            main_img_save_path = '%s/%s_%s.png' % (self.parse_img_dic_path, self.file_name, layer.name)
            self.psd_parse_info.main_img_path = main_img_save_path
            self.psd_parse_info.main_img_width = layer.width
            self.psd_parse_info.main_img_height = layer.height
            layer_image = layer.composite()
            layer_image.save(main_img_save_path)
            logger.info("[*] 主图层解析后获取的图片存储在: %s" % main_img_save_path)
            logger.info("[*] 主图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 主图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_main_border(self, layer):
        try:
            if layer.kind != 'pixel':
                logger.error('[*] 主边框图层类型错误')
                return
            logger.info("[*] 主边框图层开始解析")
            main_border_img_save_path = '%s/%s_%s.png' % (self.parse_img_dic_path, self.file_name, layer.name)
            layer_image = layer.composite()
            layer_image.save(main_border_img_save_path)
            main_border_img = Image.open(main_border_img_save_path)
            main_border_color = main_border_img.getpixel((int(main_border_img.width / 2), 2))
            main_border_color = rgb_to_hex(main_border_color)
            self.psd_parse_info.main_border_color = main_border_color
            logger.info("[*] 主边框图层颜色: %s" % main_border_color)
            logger.info("[*] 主边框图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 主边框图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_main_border_gradient_coordinate(self, layer):
        try:
            if layer.kind != 'type':
                logger.error('[*] 主边框渐变坐标图层类型错误')
                return
            logger.info("[*] 主边框渐变坐标图层开始解析")
            main_border_gradient_coordinate_text = layer.text
            coordinates = main_border_gradient_coordinate_text.split(",")
            for coordinate in coordinates:
                xy = coordinate.split('#')
                x = xy[0]
                y = xy[1]
                self.psd_parse_info.main_border_gradient_coordinates.append((int(x), int(y)))
            logger.info("[*] 主边框渐变坐标: %s" % self.psd_parse_info.main_border_gradient_coordinates.__str__())
            logger.info("[*] 主边框渐变坐标图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 主边框渐变坐标图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_main_border_gradient(self, layer):
        try:
            if layer.kind != 'pixel':
                logger.error('[*] 主边框渐变图层类型错误')
                return
            logger.info("[*] 主边框渐变图层开始解析")
            main_border_gradient_img_save_path = '%s/%s_%s.png' % (self.parse_img_dic_path, self.file_name, layer.name)
            layer_image = layer.composite()
            layer_image.save(main_border_gradient_img_save_path)
            main_border_gradient_img = Image.open(main_border_gradient_img_save_path)
            if not self.psd_parse_info.main_border_gradient_coordinates or \
                len(self.psd_parse_info.main_border_gradient_coordinates) <= 0:
                self.psd_parse_info.main_border_gradient_coordinates = []
                self.psd_parse_info.main_border_gradient_coordinates\
                    .append((int(main_border_gradient_img.width / 2), 5))
                self.psd_parse_info.main_border_gradient_coordinates\
                    .append((int(main_border_gradient_img.width / 2), main_border_gradient_img.height - 5))
                logger.info('[*] 主边框渐变坐标: %s' % self.psd_parse_info.main_border_gradient_coordinates.__str__())
            for coordinate in self.psd_parse_info.main_border_gradient_coordinates:
                color = main_border_gradient_img.getpixel(coordinate)
                color = rgb_to_hex(color)
                self.psd_parse_info.main_border_gradient_colors.append(color)
            logger.info("[*] 主边框渐变图层颜色: %s" % self.psd_parse_info.main_border_gradient_colors.__str__())
            logger.info("[*] 主边框渐变图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 主边框渐变图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_main_border_text(self, layer):
        try:
            if layer.kind != 'type':
                logger.error('[*] 主边框文字图层类型错误')
                return
            logger.info("[*] 主边框文字图层开始解析")
            main_border_text = layer.text
            self.psd_parse_info.main_border_text = main_border_text
            logger.info("[*] 主边框文字图层内容: %s" % main_border_text)
            logger.info("[*] 主边框文字图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 主边框文字图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_main_border_logo(self, layer):
        try:
            if layer.kind != 'pixel':
                logger.error('[*] 主边框logo图层类型错误')
                return
            logger.info("[*] 主边框logo图层开始解析")
            main_border_logo_save_path = '%s/%s_%s.png' % (self.parse_img_dic_path, self.file_name, layer.name)
            self.psd_parse_info.main_border_logo_path = main_border_logo_save_path
            self.psd_parse_info.main_border_logo_width = layer.width
            self.psd_parse_info.main_border_logo_height = layer.height
            layer_image = layer.composite()
            layer_image.save(main_border_logo_save_path)
            logger.info("[*] 主边框logo图层解析后获取的图片存储在: %s" % main_border_logo_save_path)
            logger.info("[*] 主边框logo图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 主边框logo图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_camera_border(self, layer):
        try:
            if layer.kind != 'pixel':
                logger.error('[*] 摄像头边框图层类型错误')
                return
            logger.info("[*] 摄像头边框图层开始解析")
            camera_border_img_save_path = '%s/%s_%s.png' % (self.parse_img_dic_path, self.file_name, layer.name)
            layer_image = layer.composite()
            layer_image.save(camera_border_img_save_path)
            camera_border_img = Image.open(camera_border_img_save_path)
            camera_border_color = camera_border_img.getpixel((int(camera_border_img.width / 2), 2))
            camera_border_color = rgb_to_hex(camera_border_color)
            self.psd_parse_info.camera_border_color = camera_border_color
            logger.info("[*] 摄像头边框图层颜色: %s" % camera_border_color)
            logger.info("[*] 摄像头边框图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 摄像头边框图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_camera_border_gradient_coordinate(self, layer):
        try:
            if layer.kind != 'type':
                logger.error('[*] 摄像头边框渐变坐标图层类型错误')
                return
            logger.info("[*] 摄像头边框渐变坐标图层开始解析")
            camera_border_gradient_coordinate_text = layer.text
            coordinates = camera_border_gradient_coordinate_text.split(",")
            for coordinate in coordinates:
                xy = coordinate.split('#')
                x = xy[0]
                y = xy[1]
                self.psd_parse_info.camera_border_gradient_coordinates.append((int(x), int(y)))
            logger.info("[*] 摄像头边框渐变坐标: %s" % self.psd_parse_info.camera_border_gradient_coordinates.__str__())
            logger.info("[*] 摄像头边框渐变坐标图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 摄像头边框渐变坐标图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_camera_border_gradient(self, layer):
        try:
            if layer.kind != 'pixel':
                logger.error('[*] 摄像头边框渐变图层类型错误')
                return
            logger.info("[*] 摄像头边框渐变图层开始解析")
            camera_border_gradient_img_save_path = '%s/%s_%s.png' % \
                                                   (self.parse_img_dic_path, self.file_name, layer.name)
            layer_image = layer.composite()
            layer_image.save(camera_border_gradient_img_save_path)
            camera_border_gradient_img = Image.open(camera_border_gradient_img_save_path)

            if not self.psd_parse_info.camera_border_gradient_coordinates or \
                len(self.psd_parse_info.camera_border_gradient_coordinates) <= 0:
                self.psd_parse_info.camera_border_gradient_coordinates = []
                self.psd_parse_info.camera_border_gradient_coordinates\
                    .append((int(camera_border_gradient_img.width / 2), 5))
                self.psd_parse_info.camera_border_gradient_coordinates\
                    .append((int(camera_border_gradient_img.width / 2), camera_border_gradient_img.height - 5))
                logger.info('[*] 摄像头边框渐变坐标: %s' % self.psd_parse_info.main_border_gradient_coordinates.__str__())
            for coordinate in self.psd_parse_info.camera_border_gradient_coordinates:
                color = camera_border_gradient_img.getpixel(coordinate)
                color = rgb_to_hex(color)
                self.psd_parse_info.camera_border_gradient_colors.append(color)
            logger.info("[*] 摄像头边框渐变图层颜色: %s" % self.psd_parse_info.camera_border_gradient_colors.__str__())
            logger.info("[*] 摄像头边框渐变图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 摄像头边框渐变图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_camera_border_text(self, layer):
        try:
            if layer.kind != 'type':
                logger.error('[*] 摄像头边框文字图层类型错误')
                return
            logger.info("[*] 摄像头边框文字图层开始解析")
            camera_border_text = layer.text
            self.psd_parse_info.camera_border_text = camera_border_text

            logger.info("[*] 摄像头边框文字图层内容: %s" % camera_border_text)
            logger.info("[*] 摄像头边框文字图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 摄像头边框文字图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_camera_border_logo(self, layer):
        try:
            if layer.kind != 'pixel':
                logger.error('[*] 摄像头边框logo图层类型错误')
                return
            logger.info("[*] 摄像头边框logo图层开始解析")
            camera_border_logo_save_path = '%s/%s_%s.png' % (self.parse_img_dic_path, self.file_name, layer.name)
            self.psd_parse_info.camera_border_logo_path = camera_border_logo_save_path
            self.psd_parse_info.camera_border_logo_width = layer.width
            self.psd_parse_info.camera_border_logo_height = layer.height
            layer_image = layer.composite()
            layer_image.save(camera_border_logo_save_path)
            logger.info("[*] 摄像头边框logo图层解析后获取的图片存储在: %s" % camera_border_logo_save_path)
            logger.info("[*] 摄像头边框logo图层解析成功完成")
            logger.info("[*] ")
        except Exception as e:
            logger.error('[*] 摄像头边框logo图层解析错误: %s' % repr(e))
            logger.info("[*] ")

    def __parse_camera_lens(self, layer):
        try:
            if layer.kind != 'pixel':
                logger.error('[*] 摄像头镜头图层类型错误')
                return
            logger.info("[*] 摄像头镜头图层开始解析")
            camera_lens_img_save_path = '%s/%s_%s.png' % (self.parse_img_dic_path, self.file_name, layer.name)
            layer_image = layer.composite()
            layer_image.save(camera_lens_img_save_path)
            camera_lens_img = Image.open(camera_lens_img_save_path)
            camera_lens_color = camera_lens_img\
                .getpixel((int(camera_lens_img.width / 2), int(camera_lens_img.height / 2)))
            camera_lens_color = rgb_to_hex(camera_lens_color)
            logger.info("[*] 摄像头镜头图层%s颜色: %s" % (layer.name, camera_lens_color))
            logger.info("[*] 摄像头镜头图层解析成功完成")
            logger.info("[*] ")
            return camera_lens_color
        except Exception as e:
            logger.error('[*] 摄像头镜头图层解析错误: %s' % repr(e))
            logger.info("[*] ")
            return ''


if __name__ == '__main__':
    psd_parser = PsdParser(psd_file_path='/Users/patrick/PycharmProjects/ex_lion/aaa2210210007.psd',
                           parse_img_dic_path='/Users/patrick/Downloads/ex_lion/res/img/parse')
    psd_parse_info = psd_parser.parse()
    logger.info('[*] psd 解析结果: %s' % psd_parse_info.__str__())
