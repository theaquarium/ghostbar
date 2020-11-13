'''
Rainbow gradient effect
'''

import colorsys
import math
import random
from effect_base import EffectBase

class RainbowGradientEffect(EffectBase):
    '''
    Rainbow gradient effect
    '''

    RANDOM_SIZE = 2

    def __init__(self, rows, cols, colors=[(255, 255, 255)], speed=0.1, angle=45, width=15):
        super().__init__(rows, cols)

        self.speed = speed
        self.colors = colors
        self.angle = math.radians(angle)
        self.width = width

        self.rainbow_counter = 0

        if angle < 0:
            self.angle_reversed = True
        else:
            self.angle_reversed = False

        if speed < 0:
            self.speed_reversed = True
        else:
            self.speed_reversed = False
            self.colors.reverse()

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
                if self.angle_reversed:
                    if len(self.stops) < 2 or index == (len(self.stops) - 1) or self.stops[index + 1]['pos'] >= 0:
                        new_stops.append(new_loc)
                else:
                    max_y = math.tan(self.angle) * self.rows
                    if len(self.stops) < 2 or index == (len(self.stops) - 1) or self.stops[index + 1]['pos'] >= -max_y:
                        new_stops.append(new_loc)
            else:
                if self.angle_reversed:
                    max_y = math.tan(self.angle) * self.rows
                    if len(self.stops) < 2 or index == 0 or self.stops[index - 1]['pos'] <= self.cols - max_y:
                        new_stops.append(new_loc)
                else:
                    if len(self.stops) < 2 or index == 0 or self.stops[index - 1]['pos'] <= self.cols:
                        new_stops.append(new_loc)

        self.stops = new_stops

    def get_pixel(self, x_coord, y_coord):
        '''
        Get color val at specific pixel
        '''
        x_diff = math.tan(self.angle) * y_coord
        stop_loc = x_coord - x_diff
        if len(self.stops) == 0:
            if self.speed_reversed:
                if self.angle_reversed:
                    self.stops.append({ 'pos': 0, 'col': self._get_rainbow_col() })
                else:
                    max_y = math.tan(self.angle) * self.rows
                    self.stops.append({ 'pos': -max_y, 'col': self._get_rainbow_col() })
            else:
                if self.angle_reversed:
                    max_y = math.tan(self.angle) * self.rows
                    self.stops.insert(0, { 'pos': self.cols - max_y, 'col': self._get_rainbow_col() })
                else:
                    self.stops.insert(0, { 'pos': self.cols, 'col': self._get_rainbow_col() })

        if self.speed_reversed:
            while stop_loc >= self.stops[-1]['pos']:
                stop_offset = self.width + ((random.random() * self.RANDOM_SIZE) - (self.RANDOM_SIZE / 2))
                self.stops.append({ 'pos': self.stops[-1]['pos'] + stop_offset, 'col': self._get_rainbow_col() })
        else:
            while stop_loc <= self.stops[0]['pos']:
                stop_offset = self.width + ((random.random() * self.RANDOM_SIZE) - (self.RANDOM_SIZE / 2))
                self.stops.insert(0, { 'pos': self.stops[0]['pos'] - stop_offset, 'col': self._get_rainbow_col() })

        stop1 = {}
        stop2 = {}
        check_next = False

        if self.speed_reversed:
            for stop in reversed(self.stops):
                if check_next:
                    if stop_loc >= stop['pos']:
                        stop2 = stop
                        break
                    check_next = False
                if stop_loc > stop['pos']:
                    continue
                stop1 = stop
                check_next = True
        else:
            for stop in self.stops:
                if check_next:
                    if stop_loc <= stop['pos']:
                        stop2 = stop
                        break
                    check_next = False
                if stop_loc < stop['pos']:
                    continue
                stop1 = stop
                check_next = True

        stop_diff = stop2['pos'] - stop1['pos']
        stop_loc_diff = stop_loc - stop1['pos']
        stop_ratio = stop_loc_diff / stop_diff
        r_diff = stop2['col'][0] - stop1['col'][0]
        g_diff = stop2['col'][1] - stop1['col'][1]
        b_diff = stop2['col'][2] - stop1['col'][2]

        return (
                stop1['col'][0] + r_diff * stop_ratio,
                stop1['col'][1] + g_diff * stop_ratio,
                stop1['col'][2] + b_diff * stop_ratio
        )

    def _get_rainbow_col(self):
        col = self.colors[self.rainbow_counter]
        self.rainbow_counter = (self.rainbow_counter + 1) % len(self.colors)
        return col
