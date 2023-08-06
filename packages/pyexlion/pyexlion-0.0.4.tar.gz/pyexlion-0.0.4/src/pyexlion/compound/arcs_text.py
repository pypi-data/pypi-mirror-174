#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw


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


if __name__ == '__main__':
    font = ImageFont.truetype('/Users/patrick/PycharmProjects/ex_lion/fonts/Arial-Bold.ttf',
                              size=28, encoding='utf-8')
    text_save_path = "/Users/patrick/Downloads/ex_lion/res/img/compound/arcs_text.png"
    arcs_text = ArcsText(border_radius=150, text_font=font, text='example', text_rotate_angle=0, text_color='#000000')
    arcs_text.draw()
    arcs_text.save(save_path=text_save_path)
