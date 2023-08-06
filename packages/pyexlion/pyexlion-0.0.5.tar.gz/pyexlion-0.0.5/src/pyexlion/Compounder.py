#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import math
from pygalaxy import ConvertMaster
from PIL import Image, ImageDraw, ImageFont
from PsdParseInfo import PsdParseInfo
import logger


def get_right_triangle_side(hypotenuse):
    return math.sqrt(pow(hypotenuse, 2) / 2)


class ImgCompounder:

    def __init__(self, psd_parse_info: PsdParseInfo, template,
                 history_id: str,
                 compound_img_dir_path: str,
                 compound_img_dir_url: str,
                 font_path: str):
        self.psd_parse_info = psd_parse_info
        self.history_id = history_id
        self.compound_dir_path = compound_img_dir_path
        self.compound_img_dir_url = compound_img_dir_url
        self.font_path = font_path
        assert os.path.exists(self.compound_dir_path), '合成图文件夹路径不存在'
        if self.history_id and len(self.history_id) > 0:
            self.compound_dir_path = self.compound_dir_path + "/" + self.history_id
            if not os.path.exists(self.compound_dir_path):
                os.mkdir(self.compound_dir_path)
        self.template_group_code = 'gcode'
        if template and 'groupCode' in template:
            self.template_group_code = template['groupCode']
        self.template_nick_name = 'nickname'
        if template and 'nickname' in template:
            self.template_nick_name = template['nickname']
        self.psd_file_name = psd_parse_info.file_path.split('/')[-1].split(".")[0]
        self.compound_file_name = '%s_%s_%s' % (self.template_group_code, self.template_nick_name, self.psd_file_name)
        self.compound_file_path = '%s/%s.png' % (self.compound_dir_path, self.compound_file_name)
        self.dpi = (300, 300)
        if template:
            # 主边框相关尺寸
            if 'frameWidth' in template:
                self.frame_width = template['frameWidth']
            if 'frameHeight' in template:
                self.frame_height = template['frameHeight']
            if 'mainBorderRadius' in template:
                self.main_border_radius = template['mainBorderRadius']
            if 'mainBorderStrokeWidth' in template:
                self.main_border_stroke_width = template['mainBorderStrokeWidth']
            if 'mainBorderTextList' in template:
                self.main_border_text_list = template['mainBorderTextList']
            if 'mainBorderLogoList' in template:
                self.main_border_logo_list = template['mainBorderLogoList']
            if 'mainBorderLeft' in template:
                self.main_border_left = template['mainBorderLeft']
            if 'mainBorderTop' in template:
                self.main_border_top = template['mainBorderTop']
            if 'mainBorderWidth' in template:
                self.main_border_width = template['mainBorderWidth']
            if 'mainBorderHeight' in template:
                self.main_border_height = template['mainBorderHeight']
            # 摄像头边框相关尺寸
            if 'cameraBorderRadius' in template:
                self.camera_border_radius = template['cameraBorderRadius']
            if 'cameraBorderStrokeWidth' in template:
                self.camera_border_stroke_width = template['cameraBorderStrokeWidth']
            if 'cameraBorderTextList' in template:
                self.camera_border_text_list = template['cameraBorderTextList']
            if 'cameraBorderLogoList' in template:
                self.camera_border_logo_list = template['cameraBorderLogoList']
            if 'cameraBorderLeft' in template:
                self.camera_border_left = template['cameraBorderLeft']
            if 'cameraBorderTop' in template:
                self.camera_border_top = template['cameraBorderTop']
            if 'cameraBorderWidth' in template:
                self.camera_border_width = template['cameraBorderWidth']
            if 'cameraBorderHeight' in template:
                self.camera_border_height = template['cameraBorderHeight']
            # 摄像头镜头相关尺寸
            if 'cameraLensList' in template:
                self.camera_lens_list = template['cameraLensList']
        else:
            self.frame_width = 924
            self.frame_height = 1898
            self.main_border_width = 924
            self.main_border_height = 1898
            self.main_border_left = 0
            self.main_border_top = 0
            self.main_border_radius = 150
            self.main_border_stroke_width = 50
            self.main_border_text_list = [
                {
                    'left': 500,
                    'top': 500,
                    'angle': 0,
                    'flip': 0
                },
                {
                    'left': 500,
                    'top': 500,
                    'angle': 45,
                    'flip': 1
                },
                {
                    'left': 500,
                    'top': 500,
                    'angle': 90,
                    'flip': 0
                },
                {
                    'left': 500,
                    'top': 500,
                    'angle': 135,
                    'flip': 1
                },
                {
                    'left': 300,
                    'top': 500,
                    'angle': 180,
                    'flip': 0
                },
                {
                    'left': 400,
                    'top': 500,
                    'angle': 225,
                    'flip': 1
                },
                {
                    'left': 400,
                    'top': 500,
                    'angle': 270,
                    'flip': 0
                },
                {
                    'left': 400,
                    'top': 500,
                    'angle': 315,
                    'flip': 1
                },
            ]
            self.main_border_logo_list = [
                {
                    'left': 500,
                    'top': 0,
                    'angle': 0
                },
                {
                    'left': 500,
                    'top': 500,
                    'angle': 45
                },
                {
                    'left': 500,
                    'top': 800,
                    'angle': 90
                },
                {
                    'left': 500,
                    'top': 800,
                    'angle': 135
                },
                {
                    'left': 400,
                    'top': 800,
                    'angle': 180
                },
                {
                    'left': 500,
                    'top': 800,
                    'angle': 225
                },
                {
                    'left': 500,
                    'top': 800,
                    'angle': 270
                },
                {
                    'left': 500,
                    'top': 800,
                    'angle': 315
                },
            ]
            self.camera_border_width = 502
            self.camera_border_height = 522
            self.camera_border_left = 12
            self.camera_border_top = 12
            self.camera_border_radius = 118
            self.camera_border_stroke_width = 46
            self.camera_border_text_list = [
                {
                    'left': 180,
                    'top': 500,
                    'angle': 0,
                    'flip': 1
                },
                {
                    'left': 500,
                    'top': 500,
                    'angle': 45,
                    'flip': 1
                },
                {
                    'left': 500,
                    'top': 180,
                    'angle': 90,
                    'flip': 1
                },
                {
                    'left': 500,
                    'top': 500,
                    'angle': 135,
                    'flip': 1
                },
                {
                    'left': 180,
                    'top': 500,
                    'angle': 180,
                    'flip': 1
                },
                {
                    'left': 400,
                    'top': 500,
                    'angle': 225,
                    'flip': 1
                },
                {
                    'left': 400,
                    'top': 180,
                    'angle': 270,
                    'flip': 1
                },
                {
                    'left': 400,
                    'top': 500,
                    'angle': 315,
                    'flip': 1
                },
            ]
            self.camera_border_logo_list = [
                {
                    'left': 250,
                    'top': 0,
                    'angle': 0
                },
                {
                    'left': 500,
                    'top': 500,
                    'angle': 45
                },
                {
                    'left': 500,
                    'top': 250,
                    'angle': 90
                },
                {
                    'left': 500,
                    'top': 800,
                    'angle': 135
                },
                {
                    'left': 250,
                    'top': 800,
                    'angle': 180
                },
                {
                    'left': 500,
                    'top': 200,
                    'angle': 225
                },
                {
                    'left': 500,
                    'top': 250,
                    'angle': 270
                },
                {
                    'left': 500,
                    'top': 800,
                    'angle': 315
                },
            ]
            self.camera_lens_list = [
                {
                    'left': 100,
                    'top': 60,
                    'radius': 90,
                },
                {
                    'left': 100,
                    'top': 260,
                    'radius': 90,
                },
                {
                    'left': 280,
                    'top': 170,
                    'radius': 90,
                },
            ]
        self.compound_img = Image.new(size=(self.frame_width, self.frame_height), mode='RGBA')
        self.compound_img.save(self.compound_file_path)

    def draw(self):
        logger.info('[*]')
        self.__drawMainImage()
        self.__drawMainBorder()
        self.__drawMainBorderGradient()
        self.__drawMainBorderText()
        self.__drawMainBorderLogo()
        self.__drawCameraBorder()
        self.__drawCameraBorderGradient()
        self.__drawCameraBorderText()
        self.__drawCameraBorderLogo()
        self.__drawCameraLens()
        # self.__to_cmyk()
        compound_result_data = {
            'path': self.compound_file_path,
            'url': '%s/%s/%s.png' % (self.compound_img_dir_url, self.history_id, self.compound_file_name)
        }
        return compound_result_data

    def __drawMainImage(self):
        try:
            logger.info('[*] 主图开始绘制')
            with Image.open(self.compound_file_path) as compound_img:
                main_img = Image.open(self.psd_parse_info.main_img_path)
                main_img = main_img.crop((1, 1, main_img.size[0] - 1, main_img.size[1] - 1))
                left = (self.frame_width - main_img.size[0]) / 2
                top = (self.frame_height - main_img.size[1]) / 2
                compound_img.paste(main_img, (int(left), int(top)))
                compound_img.save(self.compound_file_path, dpi=self.dpi)
                logger.info('[*] 主图绘制成功')
                logger.info('[*]')
        except Exception as e:
            logger.error('[*] 主图绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawMainBorder(self):
        try:
            if self.psd_parse_info.main_border_gradient_colors and \
                    len(self.psd_parse_info.main_border_gradient_colors) > 0:
                logger.info('[*] 主边框绘制渐变图层，不需要绘制纯色图层')
                logger.info('[*]')
                return
            if not self.psd_parse_info.main_border_color or len(self.psd_parse_info.main_border_color) != 7:
                logger.error('[*] 主边框颜色信息错误')
                logger.error('[*]')
                return
            logger.info('[*] 主边框开始绘制')
            scale = 5
            border_image = Image.new(size=(self.main_border_width * scale, self.main_border_height * scale),
                                     mode='RGBA')
            draw = ImageDraw.Draw(border_image)
            draw.rounded_rectangle((0, 0, self.main_border_width * scale, self.main_border_height * scale),
                                   radius=self.main_border_radius * scale,
                                   outline=self.psd_parse_info.main_border_color,
                                   width=self.main_border_stroke_width * scale)
            border_image = border_image.resize((self.main_border_width, self.main_border_height), resample=Image.BILINEAR)
            with Image.open(self.compound_file_path) as compound_img:
                compound_img.paste(border_image, (self.main_border_left, self.main_border_top), border_image)
                compound_img.save(self.compound_file_path, dpi=self.dpi)
                logger.info('[*] 主边框绘制成功')
                logger.info('[*]')
        except Exception as e:
            logger.error('[*] 主边框绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawMainBorderGradient(self):
        try:
            if not self.psd_parse_info.main_border_gradient_colors or \
                    len(self.psd_parse_info.main_border_gradient_colors) <= 0:
                logger.error('[*] 主边框渐变颜色信息错误')
                logger.error('[*]')
                return
            logger.info('[*] 主边框渐变开始绘制')
            scale = 2
            border_gradient_image = Image.new(size=(self.main_border_width * scale, self.main_border_height * scale),
                                              mode='RGBA')
            draw = ImageDraw.Draw(border_gradient_image)
            draw.rounded_rectangle((0, 0, self.main_border_width * scale, self.main_border_height * scale),
                                   radius=self.main_border_radius * scale,
                                   outline=self.psd_parse_info.main_border_gradient_colors[0],
                                   width=self.main_border_stroke_width * scale)
            pre_gradient_height = round(
                self.main_border_height * 2 / (len(self.psd_parse_info.main_border_gradient_colors) - 1))
            for index in range(len(self.psd_parse_info.main_border_gradient_colors) - 1):
                start_rgb_color = ConvertMaster.hex_to_rgb(self.psd_parse_info.main_border_gradient_colors[index])
                end_rgb_color = ConvertMaster.hex_to_rgb(self.psd_parse_info.main_border_gradient_colors[index + 1])
                r_step = (end_rgb_color[0] - start_rgb_color[0]) / pre_gradient_height
                g_step = (end_rgb_color[1] - start_rgb_color[1]) / pre_gradient_height
                b_step = (end_rgb_color[2] - start_rgb_color[2]) / pre_gradient_height
                for y in range(pre_gradient_height):
                    r = round((start_rgb_color[0] + r_step * y))
                    g = round((start_rgb_color[1] + g_step * y))
                    b = round((start_rgb_color[2] + b_step * y))
                    for x in range(border_gradient_image.width):
                        if self.main_border_radius * scale < x < self.main_border_width * scale - self.main_border_radius * scale and \
                                self.main_border_radius * scale < (y + (index * pre_gradient_height)) < self.main_border_height * scale - self.main_border_radius * scale:
                            continue
                        current_rgba = border_gradient_image.getpixel((x, y + (index * pre_gradient_height)))
                        if current_rgba[3] != 0:
                            draw.point((x, y + (index * pre_gradient_height)), fill=(r, g, b))
            border_gradient_image = border_gradient_image.resize((self.main_border_width, self.main_border_height),
                                                                 resample=Image.BICUBIC)
            with Image.open(self.compound_file_path) as compound_img:
                compound_img.paste(border_gradient_image, (self.main_border_left, self.main_border_top), border_gradient_image)
                compound_img.save(self.compound_file_path, dpi=self.dpi)
                logger.info('[*] 主边框渐变绘制成功')
                logger.info('[*]')
        except Exception as e:
            logger.error('[*] 主边框渐变绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawMainBorderText(self):
        try:
            if not self.psd_parse_info.main_border_text or len(self.psd_parse_info.main_border_text) <= 0:
                logger.error('[*] 主边框文字信息获取错误')
                logger.error('[*]')
                return
            if not self.main_border_text_list or len(self.main_border_text_list) <= 0:
                logger.error('[*] 主边框文字位置信息获取错误')
                logger.error('[*]')
                return
            text_dict_list = self.__parse_text(self.psd_parse_info.main_border_text, len(self.main_border_text_list))
            if not text_dict_list or len(text_dict_list) <= 0:
                logger.error('[*] 主边框文字解析错误')
                logger.error('[*]')
                return
            logger.info('[*] 主边框文字开始绘制')
            length = min(len(self.main_border_text_list), len(text_dict_list))
            with Image.open(self.compound_file_path) as compound_img:
                for i in range(length):
                    main_border_text = self.main_border_text_list[i]
                    text_dict = text_dict_list[i]
                    for text in text_dict:
                        color = text_dict[text]
                        if main_border_text['angle'] == 0:
                            text_image, text_width, text_height = \
                                self.__make_text_img(text=text, text_color=color,
                                                     border_stroke_width=self.main_border_stroke_width)
                            left = self.main_border_left + main_border_text['left']
                            top = self.main_border_top
                            if main_border_text['flip'] == 1:
                                text_image = text_image.rotate(180)
                                top = self.main_border_top + (self.main_border_stroke_width - text_height) / 2 + 3
                            compound_img.paste(text_image, (int(left), int(top)), text_image)
                        if main_border_text['angle'] == 45:
                            arcs_text_img = self.__draw_arcs_text_img(text=text,
                                                                      border_radius=self.main_border_radius,
                                                                      text_rotate_angle=main_border_text['angle'],
                                                                      text_color='#' + color,
                                                                      border_stroke_width=self.main_border_stroke_width)
                            if not arcs_text_img:
                                logger.error('[*] 45度弧形文字绘制出错')
                            else:
                                left = self.main_border_left + self.main_border_width - arcs_text_img.size[0]
                                top = self.main_border_top
                                compound_img.paste(arcs_text_img, (int(left), int(top)), arcs_text_img)
                        if main_border_text['angle'] == 90:
                            text_image, text_width, text_height = \
                                self.__make_text_img(text=text,
                                                     text_color=text_dict[text],
                                                     border_stroke_width=self.main_border_stroke_width)
                            left = self.main_border_left + self.main_border_width - self.main_border_stroke_width + \
                                   (self.main_border_stroke_width - text_height) / 2 + 3
                            top = self.main_border_top + main_border_text['top']
                            text_image = text_image.transpose(Image.ROTATE_270)
                            if main_border_text['flip'] == 1:
                                text_image = text_image.rotate(180)
                                left = self.main_border_left + self.main_border_width - self.main_border_stroke_width
                            compound_img.paste(text_image, (int(left), int(top)), text_image)
                        if main_border_text['angle'] == 135:
                            arcs_text_img = self.__draw_arcs_text_img(text=text,
                                                                      border_radius=self.main_border_radius,
                                                                      text_rotate_angle=main_border_text['angle'],
                                                                      text_color='#' + color,
                                                                      border_stroke_width=self.main_border_stroke_width)
                            if not arcs_text_img:
                                logger.error('[*] 135度弧形文字绘制出错')
                            else:
                                left = self.main_border_left + self.main_border_width - arcs_text_img.size[0]
                                top = self.main_border_top + self.main_border_height - arcs_text_img.size[1]
                                compound_img.paste(arcs_text_img, (int(left), int(top)), arcs_text_img)
                        if main_border_text['angle'] == 180:
                            text_image, text_width, text_height = \
                                self.__make_text_img(text=text, text_color=color,
                                                     border_stroke_width=self.main_border_stroke_width)
                            left = self.main_border_left + main_border_text['left']
                            top = self.main_border_top + self.main_border_height - self.main_border_stroke_width + \
                                  (self.main_border_stroke_width - text_height) / 2 + 3
                            text_image = text_image.transpose(Image.ROTATE_180)
                            if main_border_text['flip'] == 1:
                                text_image = text_image.rotate(180)
                                top = self.main_border_top + self.main_border_height - self.main_border_stroke_width
                            compound_img.paste(text_image, (int(left), int(top)), text_image)
                        if main_border_text['angle'] == 225:
                            arcs_text_img = self.__draw_arcs_text_img(text=text,
                                                                      border_radius=self.main_border_radius,
                                                                      text_rotate_angle=main_border_text['angle'],
                                                                      text_color='#' + color,
                                                                      border_stroke_width=self.main_border_stroke_width)
                            if not arcs_text_img:
                                logger.error('[*] 225度弧形文字绘制出错')
                            else:
                                left = self.main_border_left
                                top = self.main_border_top + self.main_border_height - arcs_text_img.size[1]
                                compound_img.paste(arcs_text_img, (int(left), int(top)), arcs_text_img)
                        if main_border_text['angle'] == 270:
                            text_image, text_width, text_height = \
                                self.__make_text_img(text=text,
                                                     text_color=text_dict[text],
                                                     border_stroke_width=self.main_border_stroke_width)
                            left = self.main_border_left
                            top = self.main_border_top + main_border_text['top']
                            text_image = text_image.transpose(Image.ROTATE_90)
                            if main_border_text['flip'] == 1:
                                text_image = text_image.rotate(180)
                                left =  self.main_border_left + (self.main_border_stroke_width - text_height) / 2 + 3
                            compound_img.paste(text_image, (int(left), int(top)), text_image)
                        if main_border_text['angle'] == 315:
                            arcs_text_img = self.__draw_arcs_text_img(text=text,
                                                                      border_radius=self.main_border_radius,
                                                                      text_rotate_angle=main_border_text['angle'],
                                                                      text_color='#' + color,
                                                                      border_stroke_width=self.main_border_stroke_width)
                            if not arcs_text_img:
                                logger.error('[*] 315度弧形文字绘制出错')
                            else:
                                left = self.main_border_left
                                top = self.main_border_top
                                compound_img.paste(arcs_text_img, (int(left), int(top)), arcs_text_img)
                compound_img.save(self.compound_file_path, dpi=self.dpi)
                logger.info('[*] 主边框文字绘制成功')
                logger.info('[*]')
        except Exception as e:
            logger.error('[*] 主边框文字绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawMainBorderLogo(self):
        try:
            if not self.psd_parse_info.main_border_logo_path or len(self.psd_parse_info.main_border_logo_path) <= 0:
                logger.error('[*] 主边框logo文件路径信息获取错误')
                logger.error('[*]')
                return
            if not self.main_border_logo_list or len(self.main_border_logo_list) <= 0:
                logger.error('[*] 主边框logo位置信息获取错误')
                logger.error('[*]')
                return
            logger.info('[*] 主边框logo开始绘制')
            with Image.open(self.compound_file_path) as compound_img:
                with Image.open(self.psd_parse_info.main_border_logo_path) as logo_img:
                    logo_offset = 4
                    aspect_rate = logo_img.size[0] / logo_img.size[1]
                    resize_height = self.main_border_stroke_width - logo_offset
                    resize_width = resize_height * aspect_rate
                    logo_img = logo_img.resize((int(resize_width), int(resize_height)))
                    right_triangle_side = get_right_triangle_side(self.main_border_radius)
                    for i in range(len(self.main_border_logo_list)):
                        main_border_logo = self.main_border_logo_list[i]
                        if main_border_logo['angle'] == 0:
                            left = self.main_border_left + main_border_logo['left']
                            top = main_border_logo['top']
                            if top <= 0:
                                top = 0 if logo_img.size[1] >= self.main_border_stroke_width else \
                                    int((self.main_border_stroke_width - logo_img.size[1]) / 2)
                            top = self.main_border_top + top
                            compound_img.paste(logo_img, (int(left), int(top)), logo_img)
                        if main_border_logo['angle'] == 45:
                            logo_img_after_rotate = logo_img.rotate(360 - 45, expand=True)
                            left = self.main_border_left + self.main_border_width - \
                                   (self.main_border_radius - right_triangle_side) - \
                                   get_right_triangle_side(logo_img.size[1]) - \
                                   get_right_triangle_side(logo_img.size[0] / 2) - logo_offset / 2
                            top = self.main_border_top + (self.main_border_radius - right_triangle_side) - \
                                  (get_right_triangle_side(logo_img.size[0] / 2)) + logo_offset / 2
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if main_border_logo['angle'] == 90:
                            logo_img_after_rotate = logo_img.rotate(360 - 90, expand=True)
                            left_offset = 0 if logo_img_after_rotate.size[0] >= self.main_border_stroke_width \
                                else (self.main_border_stroke_width - logo_img_after_rotate.size[0]) / 2
                            left = self.main_border_left + int(
                                self.main_border_width - self.main_border_stroke_width + left_offset)
                            top = self.main_border_top + main_border_logo['top']
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if main_border_logo['angle'] == 135:
                            logo_img_after_rotate = logo_img.rotate(360 - 135, expand=True)
                            left = self.main_border_left + self.main_border_width - \
                                   (self.main_border_radius - right_triangle_side) - \
                                   get_right_triangle_side(logo_img.size[1]) - \
                                   get_right_triangle_side(logo_img.size[0] / 2) - logo_offset / 2
                            top = self.main_border_top + self.main_border_height - \
                                  (self.main_border_radius - right_triangle_side) - \
                                  get_right_triangle_side(logo_img.size[1]) - \
                                  get_right_triangle_side(logo_img.size[0] / 2) - logo_offset / 2
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if main_border_logo['angle'] == 180:
                            logo_img_after_rotate = logo_img.rotate(360 - 180, expand=True)
                            left = self.main_border_left + main_border_logo['left']
                            top_offset = 0 if logo_img_after_rotate.size[1] >= self.main_border_stroke_width \
                                else (self.main_border_stroke_width - logo_img_after_rotate.size[1]) / 2
                            top = self.main_border_top + self.main_border_height - self.main_border_stroke_width + top_offset
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if main_border_logo['angle'] == 225:
                            logo_img_after_rotate = logo_img.rotate(360 - 225, expand=True)
                            left = self.main_border_left + (self.main_border_radius - right_triangle_side) - \
                                   get_right_triangle_side(logo_img.size[0] / 2) + logo_offset / 2
                            top = self.main_border_top + self.main_border_height - \
                                  (self.main_border_radius - right_triangle_side) - \
                                  get_right_triangle_side(logo_img.size[0] / 2) - \
                                  get_right_triangle_side(logo_img.size[1]) - logo_offset / 2
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if main_border_logo['angle'] == 270:
                            logo_img_after_rotate = logo_img.rotate(360 - 270, expand=True)
                            left = self.main_border_left + (
                                0 if logo_img_after_rotate.size[0] >= self.main_border_stroke_width else
                                int((self.main_border_stroke_width - logo_img_after_rotate.size[0]) / 2))
                            top = self.main_border_top + main_border_logo['top']
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if main_border_logo['angle'] == 315:
                            logo_img_after_rotate = logo_img.rotate(360 - 315, expand=True)
                            left = self.main_border_left + (self.main_border_radius - right_triangle_side) - \
                                   get_right_triangle_side(logo_img.size[0] / 2) + logo_offset / 2
                            top = self.main_border_top + (self.main_border_radius - right_triangle_side) - \
                                  get_right_triangle_side(logo_img.size[0] / 2) + logo_offset / 2
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                    compound_img.save(self.compound_file_path, dpi=self.dpi)
                    logger.info('[*] 主边框logo绘制成功')
                    logger.info('[*]')
        except Exception as e:
            logger.error('[*] 主边框logo绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawCameraBorder(self):
        try:
            if self.psd_parse_info.camera_border_gradient_colors and \
                    len(self.psd_parse_info.camera_border_gradient_colors) > 0:
                logger.info('[*] 摄像头边框绘制渐变图层，不需要绘制纯色图层')
                logger.info('[*]')
                return
            if not self.psd_parse_info.camera_border_color and len(self.psd_parse_info.camera_border_color) != 7:
                logger.error('[*] 摄像头边框颜色信息错误')
                return
            logger.info('[*] 摄像头边框开始绘制')
            scale = 5
            border_image = Image.new(size=(self.camera_border_width * scale, self.camera_border_height * scale),
                                     mode='RGBA')
            draw = ImageDraw.Draw(border_image)
            draw.rounded_rectangle((0,
                                    0,
                                    self.camera_border_width * scale,
                                    self.camera_border_height * scale),
                                   radius=self.camera_border_radius * scale,
                                   outline=self.psd_parse_info.camera_border_color,
                                   width=self.camera_border_stroke_width * scale)
            border_image = border_image.resize((self.camera_border_width, self.camera_border_height),
                                               resample=Image.BILINEAR)
            with Image.open(self.compound_file_path) as compound_img:
                compound_img.paste(border_image, (self.camera_border_left, self.camera_border_top), border_image)
                compound_img.save(self.compound_file_path, dpi=self.dpi)
                logger.info('[*] 摄像头边框绘制成功')
                logger.info('[*]')
        except Exception as e:
            logger.error('[*] 摄像头边框绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawCameraBorderGradient(self):
        try:
            if not self.psd_parse_info.camera_border_gradient_colors or \
                    len(self.psd_parse_info.camera_border_gradient_colors) <= 0:
                logger.error('[*] 摄像头边框渐变颜色信息错误')
                return
            logger.info('[*] 摄像头边框渐变开始绘制')
            scale = 2
            border_gradient_image = Image.new(
                size=(self.camera_border_width * scale, self.camera_border_height * scale), mode='RGBA')
            draw = ImageDraw.Draw(border_gradient_image)
            draw.rounded_rectangle((0, 0, self.camera_border_width * scale, self.camera_border_height * scale),
                                   radius=self.camera_border_radius * scale,
                                   outline=self.psd_parse_info.camera_border_gradient_colors[0],
                                   width=self.camera_border_stroke_width * scale)
            pre_gradient_height = round(
                self.camera_border_height * 2 / (len(self.psd_parse_info.camera_border_gradient_colors) - 1))
            for index in range(len(self.psd_parse_info.camera_border_gradient_colors) - 1):
                start_rgb_color = ConvertMaster.hex_to_rgb(self.psd_parse_info.camera_border_gradient_colors[index])
                end_rgb_color = ConvertMaster.hex_to_rgb(self.psd_parse_info.camera_border_gradient_colors[index + 1])
                r_step = (end_rgb_color[0] - start_rgb_color[0]) / pre_gradient_height
                g_step = (end_rgb_color[1] - start_rgb_color[1]) / pre_gradient_height
                b_step = (end_rgb_color[2] - start_rgb_color[2]) / pre_gradient_height
                for y in range(pre_gradient_height):
                    r = round((start_rgb_color[0] + r_step * y))
                    g = round((start_rgb_color[1] + g_step * y))
                    b = round((start_rgb_color[2] + b_step * y))
                    for x in range(border_gradient_image.width):
                        current_rgba = border_gradient_image.getpixel((x, y + (index * pre_gradient_height)))
                        if current_rgba[3] != 0:
                            draw.point((x, y + (index * pre_gradient_height)), fill=(r, g, b))
            border_gradient_image = border_gradient_image.resize((self.camera_border_width,
                                                                 self.camera_border_height),
                                                                 resample=Image.BILINEAR)
            with Image.open(self.compound_file_path) as compound_img:
                compound_img.paste(border_gradient_image, (self.camera_border_left, self.camera_border_top),
                                   border_gradient_image)
                compound_img.save(self.compound_file_path, dpi=self.dpi)
                logger.info('[*] 摄像头边框渐变绘制成功')
                logger.info('[*]')
        except Exception as e:
            logger.error('[*] 摄像头边框渐变绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawCameraBorderText(self):
        try:
            if not self.psd_parse_info.camera_border_text or len(self.psd_parse_info.camera_border_text) <= 0:
                logger.error('[*] 摄像头边框文字信息错误')
                return
            if not self.camera_border_text_list or len(self.camera_border_text_list) <= 0:
                logger.error('[*] 摄像头边框文字位置信息获取错误')
                return
            text_dict_list = self.__parse_text(self.psd_parse_info.camera_border_text, len(self.camera_border_text_list))
            if not text_dict_list or len(text_dict_list) <= 0:
                logger.error('[*] 摄像头边框文字解析错误')
                return
            logger.info('[*] 摄像头边框文字开始绘制')
            length = min(len(self.camera_border_text_list), len(text_dict_list))
            with Image.open(self.compound_file_path) as compound_img:
                for i in range(length):
                    camera_border_text = self.camera_border_text_list[i]
                    text_dict = text_dict_list[i]
                    for text in text_dict:
                        color = text_dict[text]
                        if camera_border_text['angle'] == 0:
                            text_image, text_width, text_height = \
                                self.__make_text_img(text=text, text_color=color,
                                                     border_stroke_width=self.camera_border_stroke_width)
                            left = camera_border_text['left'] + self.camera_border_left
                            top = 0 + self.camera_border_top
                            if camera_border_text['flip'] == 1:
                                text_image = text_image.rotate(180)
                                top = self.camera_border_top + (self.camera_border_stroke_width - text_height) / 2
                            compound_img.paste(text_image, (int(left), int(top)), text_image)
                        if camera_border_text['angle'] == 45:
                            arcs_text_img = self.__draw_arcs_text_img(text=text,
                                                                      border_radius=self.camera_border_radius,
                                                                      text_rotate_angle=camera_border_text['angle'],
                                                                      text_color='#' + color,
                                                                      border_stroke_width=self.camera_border_stroke_width)
                            if not arcs_text_img:
                                logger.error('[*] 45度弧形文字绘制出错')
                            else:
                                left = self.camera_border_left + self.camera_border_width - arcs_text_img.size[0]
                                top = self.camera_border_top + 0
                                compound_img.paste(arcs_text_img, (int(left), int(top)), arcs_text_img)
                        if camera_border_text['angle'] == 90:
                            text_image, text_width, text_height = \
                                self.__make_text_img(text=text,
                                                     text_color=text_dict[text],
                                                     border_stroke_width=self.camera_border_stroke_width)
                            left = self.camera_border_width - self.camera_border_stroke_width + \
                                   (self.camera_border_stroke_width - text_height) / 2 + 3 + self.camera_border_left
                            top = camera_border_text['top'] + self.camera_border_top
                            text_image = text_image.transpose(Image.ROTATE_270)
                            if camera_border_text['flip'] == 1:
                                text_image = text_image.rotate(180)
                                left = self.camera_border_width - self.camera_border_stroke_width + self.camera_border_left
                            compound_img.paste(text_image, (int(left), int(top)), text_image)
                        if camera_border_text['angle'] == 135:
                            arcs_text_img = self.__draw_arcs_text_img(text=text,
                                                                      border_radius=self.camera_border_radius,
                                                                      text_rotate_angle=camera_border_text['angle'],
                                                                      text_color='#' + color,
                                                                      border_stroke_width=self.camera_border_stroke_width)
                            if not arcs_text_img:
                                logger.error('[*] 135度弧形文字绘制出错')
                            else:
                                left = self.camera_border_left + self.camera_border_width - arcs_text_img.size[0]
                                top = self.camera_border_top + self.camera_border_height - arcs_text_img.size[1]
                                compound_img.paste(arcs_text_img, (int(left), int(top)), arcs_text_img)
                        if camera_border_text['angle'] == 180:
                            text_image, text_width, text_height = \
                                self.__make_text_img(text=text, text_color=color,
                                                     border_stroke_width=self.camera_border_stroke_width)
                            left = self.camera_border_left + camera_border_text['left']
                            top = self.camera_border_top + self.camera_border_height - self.camera_border_stroke_width + \
                                  (self.camera_border_stroke_width - text_height) / 2
                            text_image = text_image.transpose(Image.ROTATE_180)
                            if camera_border_text['flip'] == 1:
                                text_image = text_image.rotate(180)
                                top = self.camera_border_top + self.camera_border_height - self.camera_border_stroke_width
                            compound_img.paste(text_image, (int(left), int(top)), text_image)
                        if camera_border_text['angle'] == 225:
                            arcs_text_img = self.__draw_arcs_text_img(text=text,
                                                                      border_radius=self.camera_border_radius,
                                                                      text_rotate_angle=camera_border_text['angle'],
                                                                      text_color='#' + color,
                                                                      border_stroke_width=self.camera_border_stroke_width)
                            if not arcs_text_img:
                                logger.error('[*] 225度弧形文字绘制出错')
                            else:
                                left = self.camera_border_left + 0
                                top = self.camera_border_top + self.camera_border_height - arcs_text_img.size[1]
                                compound_img.paste(arcs_text_img, (int(left), int(top)), arcs_text_img)
                        if camera_border_text['angle'] == 270:
                            text_image, text_width, text_height = \
                                self.__make_text_img(text=text,
                                                     text_color=text_dict[text],
                                                     border_stroke_width=self.camera_border_stroke_width)
                            left = self.camera_border_left + 0
                            top = self.camera_border_top + camera_border_text['top']
                            text_image = text_image.transpose(Image.ROTATE_90)
                            if camera_border_text['flip'] == 1:
                                text_image = text_image.rotate(180)
                                left = self.camera_border_left + (self.camera_border_stroke_width - text_height) / 2
                            compound_img.paste(text_image, (int(left), int(top)), text_image)
                        if camera_border_text['angle'] == 315:
                            arcs_text_img = self.__draw_arcs_text_img(text=text,
                                                                      border_radius=self.camera_border_radius,
                                                                      text_rotate_angle=camera_border_text['angle'],
                                                                      text_color='#' + color,
                                                                      border_stroke_width=self.camera_border_stroke_width)
                            if not arcs_text_img:
                                logger.error('[*] 315度弧形文字绘制出错')
                            else:
                                left = self.camera_border_left
                                top = self.camera_border_top
                                compound_img.paste(arcs_text_img, (int(left), int(top)), arcs_text_img)
                compound_img.save(self.compound_file_path, dpi=self.dpi)
                logger.info('[*] 摄像头边框文字绘制成功')
                logger.info('[*]')
        except Exception as e:
            logger.error('[*] 摄像头边框文字绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawCameraBorderLogo(self):
        try:
            if not self.psd_parse_info.camera_border_logo_path or len(self.psd_parse_info.camera_border_logo_path) <= 0:
                logger.error('[*] 摄像头边框logo文件路径信息错误')
                return
            if not self.camera_border_logo_list or len(self.camera_border_logo_list) <= 0:
                logger.error('[*] 摄像头边框logo位置信息获取错误')
                return
            logger.info('[*] 摄像头边框logo开始绘制')
            with Image.open(self.compound_file_path) as compound_img:
                with Image.open(self.psd_parse_info.camera_border_logo_path) as logo_img:
                    logo_offset = 4
                    aspect_rate = logo_img.size[0] / logo_img.size[1]
                    resize_height = self.camera_border_stroke_width - logo_offset
                    resize_width = resize_height * aspect_rate
                    logo_img = logo_img.resize((int(resize_width), int(resize_height)))
                    right_triangle_side = get_right_triangle_side(self.camera_border_radius)
                    for i in range(len(self.camera_border_logo_list)):
                        camera_border_logo = self.camera_border_logo_list[i]
                        if camera_border_logo['angle'] == 0:
                            left = self.camera_border_left + camera_border_logo['left']
                            top = camera_border_logo['top']
                            if top <= 0:
                                top = 0 if logo_img.size[1] >= self.camera_border_stroke_width else \
                                    int((self.camera_border_stroke_width - logo_img.size[1]) / 2)
                            top = self.camera_border_top + top
                            compound_img.paste(logo_img, (left, top), logo_img)
                        if camera_border_logo['angle'] == 45:
                            logo_img_after_rotate = logo_img.rotate(360 - 45, expand=True)
                            left = self.camera_border_left + self.camera_border_width - \
                                   (self.camera_border_radius - right_triangle_side) - \
                                   get_right_triangle_side(logo_img.size[1]) - \
                                   get_right_triangle_side(logo_img.size[0] / 2) - logo_offset / 2
                            top = self.camera_border_top + (self.camera_border_radius - right_triangle_side) - \
                                  (get_right_triangle_side(logo_img.size[0] / 2)) + logo_offset / 2
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if camera_border_logo['angle'] == 90:
                            logo_img_after_rotate = logo_img.rotate(360 - 90, expand=True)
                            left_offset = 0 if logo_img_after_rotate.size[0] >= self.camera_border_stroke_width \
                                else (self.camera_border_stroke_width - logo_img_after_rotate.size[0]) / 2
                            left = self.camera_border_left + int(
                                self.camera_border_width - self.camera_border_stroke_width + left_offset)
                            top = self.camera_border_top + camera_border_logo['top']
                            compound_img.paste(logo_img_after_rotate, (left, top), logo_img_after_rotate)
                        if camera_border_logo['angle'] == 135:
                            logo_img_after_rotate = logo_img.rotate(360 - 135, expand=True)
                            left = self.camera_border_left + \
                                   self.camera_border_width - \
                                   (self.camera_border_radius - right_triangle_side) - \
                                   get_right_triangle_side(logo_img.size[1]) - \
                                   get_right_triangle_side(logo_img.size[0] / 2) - logo_offset / 2
                            top = self.camera_border_top + \
                                  self.camera_border_height - \
                                  (self.camera_border_radius - right_triangle_side) - \
                                  get_right_triangle_side(logo_img.size[1]) - \
                                  get_right_triangle_side(logo_img.size[0] / 2) - logo_offset / 2
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if camera_border_logo['angle'] == 180:
                            logo_img_after_rotate = logo_img.rotate(360 - 180, expand=True)
                            left = self.camera_border_left + camera_border_logo['left']
                            top_offset = 0 if logo_img_after_rotate.size[1] >= self.camera_border_stroke_width \
                                else (self.camera_border_stroke_width - logo_img_after_rotate.size[1]) / 2
                            top = self.camera_border_top + int(
                                self.camera_border_height - self.camera_border_stroke_width + top_offset)
                            compound_img.paste(logo_img_after_rotate, (left, top), logo_img_after_rotate)
                        if camera_border_logo['angle'] == 225:
                            logo_img_after_rotate = logo_img.rotate(360 - 225, expand=True)
                            left = self.camera_border_left + \
                                   (self.camera_border_radius - right_triangle_side) - \
                                   get_right_triangle_side(logo_img.size[0] / 2) + logo_offset / 2
                            top = self.camera_border_top + \
                                  self.camera_border_height - \
                                  (self.camera_border_radius - right_triangle_side) - \
                                  get_right_triangle_side(logo_img.size[0] / 2) - \
                                  get_right_triangle_side(logo_img.size[1]) - logo_offset / 2
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                        if camera_border_logo['angle'] == 270:
                            logo_img_after_rotate = logo_img.rotate(360 - 270, expand=True)
                            left = self.camera_border_left + (
                                0 if logo_img_after_rotate.size[0] >= self.camera_border_stroke_width \
                                    else int((self.camera_border_stroke_width - logo_img_after_rotate.size[0]) / 2))
                            top = self.camera_border_top + camera_border_logo['top']
                            compound_img.paste(logo_img_after_rotate, (left, top), logo_img_after_rotate)
                        if camera_border_logo['angle'] == 315:
                            logo_img_after_rotate = logo_img.rotate(360 - 315, expand=True)
                            left = self.camera_border_left + \
                                   (self.camera_border_radius - right_triangle_side) - \
                                   get_right_triangle_side(logo_img.size[0] / 2) + logo_offset / 2
                            top = self.camera_border_top + \
                                  (self.camera_border_radius - right_triangle_side) - \
                                  get_right_triangle_side(logo_img.size[0] / 2) + logo_offset / 2
                            compound_img.paste(logo_img_after_rotate, (int(left), int(top)), logo_img_after_rotate)
                    compound_img.save(self.compound_file_path, dpi=self.dpi)
                    logger.info('[*] 摄像头边框logo绘制成功')
                    logger.info('[*]')
        except Exception as e:
            logger.error('[*] 摄像头边框logo绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __drawCameraLens(self):
        try:
            if not self.camera_lens_list or len(self.camera_lens_list) <= 0:
                logger.error('[*] 未提供摄像头镜头模板信息，不需要绘制')
                return
            if not self.psd_parse_info.camera_lens_colors or len(self.psd_parse_info.camera_lens_colors) <= 0:
                logger.error('[*] 摄像头镜头颜色信息解析错误')
                return
            logger.info('[*] 摄像头镜头开始绘制')
            with Image.open(self.compound_file_path) as compound_img:
                length = min(len(self.psd_parse_info.camera_lens_colors), len(self.camera_lens_list))
                scale = 5
                for index in range(length):
                    camera_lens = self.camera_lens_list[index]
                    color = self.psd_parse_info.camera_lens_colors[index]
                    radius = camera_lens['radius']
                    left = camera_lens['left']
                    top = camera_lens['top']
                    circle_img = Image.new(mode='RGBA', size=(radius * 2 * scale, radius * 2 * scale))
                    draw = ImageDraw.Draw(circle_img)
                    draw.ellipse((0, 0, radius * 2 * scale, radius * 2 * scale), fill=color)
                    circle_img = circle_img.resize((radius * 2, radius * 2), resample=Image.BILINEAR)
                    compound_img.paste(circle_img, (left, top), circle_img)
                compound_img.save(self.compound_file_path, dpi=self.dpi)
                logger.info('[*] 摄像头镜头绘制成功')
                logger.info('[*]')
        except Exception as e:
            logger.error('[*] 摄像头镜头绘制错误: %s' % repr(e))
            logger.error('[*]')

    def __to_cmyk(self):
        with Image.open(self.compound_file_path) as compound_img:
            compound_img = compound_img.convert('CMYK')
            compound_img.save('%s/%s.jpeg' % (self.compound_dir_path, self.compound_file_name), dpi=self.dpi)

    def __parse_text(self, text: str, text_position_length: int):
        try:
            text_dict_list = []
            if text.startswith("m:"):
                text = text[2:]
                for tx in text.split(','):
                    if tx and len(tx) > 0:
                        txs = tx.split('#')
                        content = txs[0]
                        color = txs[1]
                        dic = {content: color}
                        text_dict_list.append(dic)
            elif text.startswith("s:"):
                text = text[2:]
                txs = text.split('#')
                color = txs[1]
                for content in txs[0].split(','):
                    dic = {content: color}
                    text_dict_list.append(dic)
            elif text.startswith("c:"):
                text = text[2:]
                txs = text.split('#')
                content = txs[0]
                color = txs[1]
                for i in range(text_position_length):
                    dic = {content: color}
                    text_dict_list.append(dic)
            else:
                logger.error('[*] 文字格式不符合要求无法解析')
                logger.error('[*]')
            return text_dict_list
        except Exception as e:
            logger.error('[*] 文字格式解析出错: %s' % repr(e))
            logger.info('[*]')
            return None

    def __make_text_img(self, text: str, text_color: str = '000000', border_stroke_width: int = 40):
        font = ImageFont.truetype(self.font_path, size=border_stroke_width - 9, encoding='utf-8')
        font_size = font.getsize(text)
        text_width = font_size[0]
        text_height = font_size[1]
        text_image = Image.new(size=(text_width, text_height), mode='RGBA')
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), text, font=font, spacing=0, fill='#' + text_color, align='left', direction='ltr')
        return text_image, text_width, text_height

    def __draw_arcs_text_img(self, text: str, border_radius: int, text_rotate_angle: int,
                             text_color: str = '000000', border_stroke_width: int = 40):
        try:
            font = ImageFont.truetype(self.font_path, size=border_stroke_width - 9, encoding='utf-8')
            arcs_text = ArcsText(border_radius=border_radius, text_font=font, text=text,
                                 text_rotate_angle=text_rotate_angle,
                                 text_color=text_color)
            arcs_text_img = arcs_text.draw()
            return arcs_text_img
        except Exception as e:
            logger.error('[*] 弧形文字绘制错误: %s' % repr(e))
            logger.error('[*]')
            return None


class ArcsText:

    def __init__(self, border_radius, text_font, text, text_rotate_angle, text_color: str = '#000000'):
        self.img = None
        self.fill = text_color
        self.R = border_radius

        self.text_font = text_font
        self.text = text
        self.text_rotate_angle = text_rotate_angle
        self.arcs_text = 90 if 90 / 10 * len(text) > 90 else 90 / 10 * len(text)
        self.font_ratio_x = 1

    def draw_rotated_text(self, image, angle, xy, r, letter, fill, font_ratio_x, font_flip=False):
        width, height = image.size
        max_dim = max(width, height)
        mask_size = (max_dim * 2, max_dim * 2)
        mask_resize = (int(max_dim * 2 * font_ratio_x), max_dim * 2)
        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask)
        textbbox = draw.textbbox((max_dim, max_dim), letter, font=self.text_font, align="center")
        font_width = textbbox[2] - textbbox[0]
        font_height = textbbox[3] - textbbox[1]
        if font_flip:
            word_pos = (int(max_dim - font_width / 2), max_dim + r - font_height)
        else:
            word_pos = (int(max_dim - font_width / 2), max_dim - r)
        draw.text(word_pos, letter, 255, font=self.text_font, align="center")
        if angle % 90 == 0:
            rotated_mask = mask.resize(mask_resize).rotate(angle)
        else:
            bigger_mask = mask.resize((int(max_dim * 8 * font_ratio_x), max_dim * 8),
                                      resample=Image.BILINEAR)
            rotated_mask = bigger_mask.rotate(angle).resize(mask_resize, resample=Image.BILINEAR)
        mask_xy = (max_dim * font_ratio_x - xy[0], max_dim - xy[1])
        b_box = mask_xy + (mask_xy[0] + width, mask_xy[1] + height)
        mask = rotated_mask.crop(b_box)
        color_image = Image.new('RGBA', image.size, fill)
        image.paste(color_image, mask)

    def draw(self):
        img = Image.new("RGBA", (2 * self.R, 2 * self.R), (255, 255, 255, 0))
        # text_bbox = self.text_font.getbbox(self.text)
        angle_word = self.arcs_text / len(self.text)
        angle_word_curr = ((len(self.text) - 1) / 2) * angle_word
        for letter in self.text:
            self.draw_rotated_text(img, angle_word_curr, (self.R, self.R), self.R, letter, self.fill, self.font_ratio_x)
            angle_word_curr = angle_word_curr - angle_word
        self.img = img.rotate(360 - self.text_rotate_angle)
        return self.img

    def save(self, save_path: str):
        self.img.save(save_path)


def t():
    image = Image.new("RGB", (200, 80))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/Users/patrick/PycharmProjects/ex_lion/fonts/Montserrat-Bold.ttf', size=30,
                              encoding='utf-8')
    bbox = draw.textbbox((20, 20), "example", font=font)
    draw.rectangle(bbox, outline="red")
    print(bbox)
    image.show()


def t2():
    image = Image.new("RGB", (200, 80))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/Users/patrick/PycharmProjects/ex_lion/fonts/Montserrat-Bold.ttf', size=30,
                              encoding='utf-8')
    xy = (20, 20)
    text = "example"
    draw.text(xy, text, font=font)
    x, y = xy
    for c in text:
        bbox = draw.textbbox((x, y), c, font=font)
        draw.rectangle(bbox, outline="red")
        x += draw.textlength(c, font=font)
    image.show()


if __name__ == '__main__':
    pass
