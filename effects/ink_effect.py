'''
Ink effect
'''

import colorsys
import random
from effect_base import EffectBase

class InkEffect(EffectBase):
    '''
    Ink effect
    '''
    def __init__(self, rows, cols, speed=0.1):
        super().__init__(rows, cols)

        self.size = 0.0
        self.speed = speed

        self.all_fg = True
        self.bg_col = rand_color()
        self.fg_col = rand_color()
        self.center = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))

    def evolve(self):
        '''
        Increase circle size by one speed unit
        '''

        if self.all_fg:
            self.bg_col = self.fg_col
            self.fg_col = rand_color()
            self.center = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
            self.size = 0.0
        self.all_fg = True

        self.size += self.speed

    def get_pixel(self, x_coord, y_coord):
        dist = (
            (x_coord - self.center[0]) ** 2 + (y_coord - self.center[1]) ** 2
        ) ** 0.5
        if dist < self.size:
            return self.fg_col
        # If not entirely foreground, set all_fg to False
        self.all_fg = False
        if dist <= self.size + 1:
            diff_ratio = abs(dist - self.size)
            r_diff = self.bg_col[0] - self.fg_col[0]
            g_diff = self.bg_col[1] - self.fg_col[1]
            b_diff = self.bg_col[2] - self.fg_col[2]
            return (
                self.fg_col[0] + r_diff * diff_ratio,
                self.fg_col[1] + g_diff * diff_ratio,
                self.fg_col[2] + b_diff * diff_ratio
            )
        return self.bg_col

    # def get_data(self, brightness=1):
    #     data = []
    #     all_fg = True
    #     for y_coord in range (0, self.rows):
    #         data.append([])
    #         for x_coord in range (0, self.cols):
    #             pixel_val = self.get_pixel(x_coord, y_coord)
    #             if pixel_val is not self.fg_col:
    #                 all_fg = False
    #             col = tuple([brightness * x for x in pixel_val])
    #             data[y_coord].append(col)

    #     if all_fg:
            # self.bg_col = self.fg_col
            # self.fg_col = rand_color()
            # self.center = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
            # self.size = 0.0

    #     return data

def rand_color():
    '''
    Generate random RGB color that's pretty bright and saturated (but not always)
    '''
    hue = random.randint(0, 255) / 255.0
    saturation = (255 - random.randint(0, 50)) / 255.0
    value = (255 - random.randint(0, 50)) / 255.0
    color_scaled = colorsys.hsv_to_rgb(hue, saturation, value)
    return tuple([255 * x for x in color_scaled])
