'''
Stars effect
'''

import colorsys
import random
import math

from effect_base import EffectBase

class FireworksEffect(EffectBase):
    '''
    Stars effect
    '''

    class Star:
        '''
        Star
        '''

        def __init__(self, x, y, age, max_age):
            self.x = x
            self.y = y
            self.age = age
            self.max_age = max_age
            self.color = FireworksEffect.Star.rand_color()

        @staticmethod
        def bang(cols, rows):
            '''
            A new star is born!
            '''
            return FireworksEffect.Star(
                    # coords
                    random.randint(1, cols - 2),
                    random.randint(1, rows - 2),
                    # current age
                    0,
                    # max age
                    random.randint(50, 100),
                ) 

        @staticmethod
        def rand_color():
            '''
            Generate random RGB color that's pretty bright and saturated (but not always)
            '''
            hue = random.randint(0, 255) / 255.0
            saturation = (255 - random.randint(0, 50)) / 255.0
            value = (255 - random.randint(0, 50)) / 255.0
            color_scaled = colorsys.hsv_to_rgb(hue, saturation, value)
            return tuple([255 * x for x in color_scaled])

    def __init__(self, rows, cols, speed=0.1, density=5):
        super().__init__(rows, cols)

        self.color = (0, 0, 0)
        self.speed = speed
        self.density = density

        self.stars = []
        self.data = [[self.color for x in range(self.cols)] for y in range(self.rows)]

        while len(self.stars) < self.density:
            self.stars.append(self.Star.bang(self.cols, self.rows))

    def evolve(self):
        '''
        Evolve the stars
        '''

        # in the beginning there was nothing ...
        new_data = [[self.color for x in range(self.cols)] for y in range(self.rows)]

        # then the stars appeared
        new_stars = []
        for star in self.stars:
            star.age += 1
            if star.age < star.max_age:
                new_star = star
            else:
                # if the star is too old, a new one should be created instead
                new_star = self.Star.bang(self.cols, self.rows)
            new_stars.append(new_star)

            age_of_maturity = new_star.max_age * 1 / 3

            # young stars are getting brighter
            if new_star.age < age_of_maturity:
                fading_ratio = new_star.age / new_star.max_age
                # add the star to the canvas
                new_data[new_star.y][new_star.x] = self.blend_colors(self.color, new_star.color, fading_ratio)

            # older stars explode and fade
            else:
                # compute the points of the rays
                ray_speed = 0.2
                dist_straight = new_star.age - age_of_maturity
                dist_diag     = dist_straight / (2 ** 0.5)
                dist_straight = int(dist_straight * ray_speed)
                dist_diag     = int(dist_diag * ray_speed)
                rays = []
                ray_length = 5
                for l in range(ray_length):
                    # straight rays (up, down, left, right)
                    if dist_straight >= 0:
                        rays.append([new_star.x,                 new_star.y - dist_straight, l])
                        rays.append([new_star.x,                 new_star.y + dist_straight, l])
                        rays.append([new_star.x - dist_straight, new_star.y,                 l])
                        rays.append([new_star.x + dist_straight, new_star.y,                 l])

                    # diagonal rays
                    if dist_diag >= 0:
                        rays.append([new_star.x - dist_diag,     new_star.y - dist_diag,     l])
                        rays.append([new_star.x - dist_diag,     new_star.y + dist_diag,     l])
                        rays.append([new_star.x + dist_diag,     new_star.y + dist_diag,     l])
                        rays.append([new_star.x + dist_diag,     new_star.y - dist_diag,     l])
                        
                    dist_straight -= 1
                    dist_diag -= 1
                
                # make sure the rays are within the canvas
                rays = [r for r in rays if 0 <= r[0] and r[0] < self.cols and 0 <= r[1] and r[1] < self.rows]

                # add rays to the canvas
                fading_ratio = 1 - 1 / (new_star.max_age - new_star.age)
                for r in rays:
                    new_data[r[1]][r[0]] = self.blend_colors(self.color, new_star.color, fading_ratio / (r[2] + 1))

        # print(new_data)
        self.stars = new_stars
        self.data = new_data

    def get_pixel(self, x_coord, y_coord):
        '''
        Get color val at specific pixel (buffer is precalculated for this effect)
        '''
        return self.data[y_coord][x_coord]

    @staticmethod
    def blend_colors(col1, col2, ratio_of_second):
        '''
        Blend between two colors
        '''
        r_diff = col2[0] - col1[0]
        g_diff = col2[1] - col1[1]
        b_diff = col2[2] - col1[2]

        return (
            col1[0] + r_diff * ratio_of_second,
            col1[1] + g_diff * ratio_of_second,
            col1[2] + b_diff * ratio_of_second
        )
