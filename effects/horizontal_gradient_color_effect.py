'''
Horizontal gradient color effect
'''

import colorsys
import math
import random

from colorable_effect_base import ColorableEffectBase

class HorizontalGradientColorEffect(ColorableEffectBase):
    '''
    Horizontal gradient color effect
    '''

    RANDOM_SIZE = 2

    def __init__(self, rows, cols, color=(255, 255, 255), speed=0.1, width=2):
        super().__init__(rows, cols)

        self.speed = speed
        self.color = color
        self.width = width

        if speed < 0:
            self.speed_reversed = True
        else:
            self.speed_reversed = False

        self.stops = []

    def evolve(self):
        '''
        Move stops over by the speed
        '''
        new_stops = []
        for (index, stop) in enumerate(self.stops):
            new_loc = {
                'pos': stop['pos'] + self.speed,
                'col': stop['col'],
            }

            if self.speed_reversed:
                if len(self.stops) < 2 or index == (len(self.stops) - 1) or self.stops[index + 1]['pos'] >= 0:
                    new_stops.append(new_loc)
            else:
                if len(self.stops) < 2 or index == 0 or self.stops[index - 1]['pos'] <= self.rows:
                    new_stops.append(new_loc)

        self.stops = new_stops

    def get_pixel(self, x_coord, y_coord):
        '''
        Get color val at specific pixel
        '''
        if len(self.stops) == 0:
            if self.speed_reversed:
                self.stops.append({ 'pos': 0, 'col': related_color(self.color) })
            else:
                self.stops.insert(0, { 'pos': self.rows, 'col': related_color(self.color) })

        if self.speed_reversed:
            while y_coord >= self.stops[-1]['pos']:
                stop_offset = self.width + ((random.random() * self.RANDOM_SIZE) - (self.RANDOM_SIZE / 2))
                self.stops.append({ 'pos': self.stops[-1]['pos'] + stop_offset, 'col': related_color(self.color) })
        else:
            while y_coord <= self.stops[0]['pos']:
                stop_offset = self.width + ((random.random() * self.RANDOM_SIZE) - (self.RANDOM_SIZE / 2))
                self.stops.insert(0, { 'pos': self.stops[0]['pos'] - stop_offset, 'col': related_color(self.color) })

        stop1 = {}
        stop2 = {}
        check_next = False

        if self.speed_reversed:
            for stop in reversed(self.stops):
                if check_next:
                    if y_coord >= stop['pos']:
                        stop2 = stop
                        break
                    check_next = False
                if y_coord > stop['pos']:
                    continue
                stop1 = stop
                check_next = True
        else:
            for stop in self.stops:
                if check_next:
                    if y_coord <= stop['pos']:
                        stop2 = stop
                        break
                    check_next = False
                if y_coord < stop['pos']:
                    continue
                stop1 = stop
                check_next = True

        stop_diff = stop2['pos'] - stop1['pos']
        stop_loc_diff = y_coord - stop1['pos']
        stop_ratio = stop_loc_diff / stop_diff
        r_diff = stop2['col'][0] - stop1['col'][0]
        g_diff = stop2['col'][1] - stop1['col'][1]
        b_diff = stop2['col'][2] - stop1['col'][2]

        return (
                stop1['col'][0] + r_diff * stop_ratio,
                stop1['col'][1] + g_diff * stop_ratio,
                stop1['col'][2] + b_diff * stop_ratio
        )


def clamp(num, minn, maxn):
    '''
    Clamp int to range
    '''
    return max(min(maxn, num), minn)

def related_color(color):
    '''
    Get a similar color
    '''
    color_scaled = tuple([x / 255 for x in color])
    hsv_col = colorsys.rgb_to_hsv(*color_scaled)
    # add plusminus 20 to hue
    new_hue = (hsv_col[0] + ((random.randint(0, 40) - 20) / 255.0)) % 1.0
    new_sat = clamp(hsv_col[1] * 255 + (random.randint(0, 40) - 20), 0, 255) / 255
    new_val = clamp(hsv_col[2] * 255 + (random.randint(0, 40) - 20), 0, 255) / 255
    new_color = colorsys.hsv_to_rgb(new_hue, new_sat, new_val)
    return tuple([255 * x for x in new_color])
