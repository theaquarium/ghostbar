'''
Rain effect
'''

import random
import math

from colorable_effect_base import ColorableEffectBase

class RainEffect(ColorableEffectBase):
    '''
    Rain effect
    '''

    BUFFER_SIZE = 2
    INITIAL_Y_RANDOMIZER = 1

    def __init__(self, rows, cols, color=(255, 255, 255), particle_color=(255, 255, 255), speed=0.1, density=100):
        super().__init__(rows, cols)

        self.color = color
        self.particle_color = particle_color
        self.speed = speed
        self.density = density

        self.particles = []
        self.data = [[self.color for x in range(self.cols)] for y in range(self.rows)]

        while len(self.particles) < self.density:
            self.particles.append((
                random.randint(0, self.cols - 1),
                random.uniform(-self.BUFFER_SIZE, (self.rows - 1) + self.BUFFER_SIZE) + random.uniform(-self.INITIAL_Y_RANDOMIZER, self.INITIAL_Y_RANDOMIZER)
            ))

    def evolve(self):
        '''
        Precipitate particles by speed
        '''
        new_data = [[self.color for x in range(self.cols)] for y in range(self.rows)]
        new_particles = []
        for particle in self.particles:
            new_particle = (particle[0], particle[1] + self.speed)
            if new_particle[1] > (self.rows - 1) + self.BUFFER_SIZE:
                new_particle = (
                    random.randint(0, self.cols - 1),
                    - self.BUFFER_SIZE + random.uniform(-self.INITIAL_Y_RANDOMIZER, self.INITIAL_Y_RANDOMIZER)
                )
            new_particles.append(new_particle)

            # Build up buffer
            particle_y = new_particle[1]
            particle_y_floor = math.floor(particle_y)
            particle_amount_in_floor = particle_y - particle_y_floor
            if particle_y_floor >= 0 and particle_y_floor < self.rows:
                blended_color_floor = blend_colors(
                    new_data[particle_y_floor][new_particle[0]],
                    self.particle_color, 1 - particle_amount_in_floor
                )
                new_data[particle_y_floor][new_particle[0]] = blended_color_floor
            if particle_y_floor + 1 >= 0 and particle_y_floor + 1 < self.rows:
                blended_color_ceiling = blend_colors(
                    new_data[particle_y_floor + 1][new_particle[0]],
                    self.particle_color, particle_amount_in_floor
                )
                new_data[particle_y_floor + 1][new_particle[0]] = blended_color_ceiling

        # print(new_data)
        self.particles = new_particles
        self.data = new_data

    def get_pixel(self, x_coord, y_coord):
        '''
        Get color val at specific pixel (buffer is precalculated for this effect)
        '''
        return self.data[y_coord][x_coord]

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
