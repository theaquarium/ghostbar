'''
Stars effect
'''

import random
import math

from colorable_effect_base import ColorableEffectBase

class StarsEffect(ColorableEffectBase):
    '''
    Stars effect
    '''

    def __init__(self, rows, cols, color=(255, 255, 255), particle_color=(255, 255, 255), points=[(0.0, 0.0), (0.42, 0.0), (0.58, 1.0), (1.0, 1.0)], speed=0.1, density=100):
        super().__init__(rows, cols)

        self.color = color
        self.particle_color = particle_color
        self.speed = speed
        self.density = density
        self.points = points

        self.particles = []
        self.data = [[self.color for x in range(self.cols)] for y in range(self.rows)]

        while len(self.particles) < self.density:
            self.particles.append((
                random.randint(0, self.cols - 1),
                random.randint(0, self.rows - 1),
                random.uniform(0, 2),
            ))

    def evolve(self):
        '''
        Evolve stars by speed
        '''
        new_data = [[self.color for x in range(self.cols)] for y in range(self.rows)]
        new_particles = []
        for particle in self.particles:
            new_particle = (particle[0], particle[1], particle[2] + self.speed)
            if new_particle[2] >= 2.0:
                new_particle = (
                    random.randint(0, self.cols - 1),
                    random.randint(0, self.rows - 1),
                    0,
                )
            new_particles.append(new_particle)

            # Build up buffer
            particle_progress = abs(1.0 - new_particle[2])
            particle_progress_diff = 1.0 - particle_progress
            term1 = scalar_multiplier(self.points[0], particle_progress_diff ** 3)
            term2 = scalar_multiplier(self.points[1], 3 * particle_progress_diff ** 2 * particle_progress)
            term3 = scalar_multiplier(self.points[2], 3 * particle_progress_diff * particle_progress ** 2)
            term4 = scalar_multiplier(self.points[3], particle_progress ** 3)
            particle_strength = 1 - (term1[1] + term2[1] + term3[1] + term4[1])
            # Star center
            if new_particle[1] >= 0 and new_particle[1] < self.rows:
                color = blend_colors(
                    new_data[new_particle[1]][new_particle[0]],
                    self.particle_color, particle_strength,
                )
                new_data[new_particle[1]][new_particle[0]] = color
            # Star top
            if new_particle[1] - 1 >= 0 and new_particle[1] - 1 < self.rows:
                color = blend_colors(
                    new_data[new_particle[1] - 1][new_particle[0]],
                    self.particle_color, particle_strength / 3,
                )
                new_data[new_particle[1] - 1][new_particle[0]] = color
            # Star bottom
            if new_particle[1] + 1 >= 0 and new_particle[1] + 1 < self.rows:
                color = blend_colors(
                    new_data[new_particle[1] + 1][new_particle[0]],
                    self.particle_color, particle_strength / 3,
                )
                new_data[new_particle[1] + 1][new_particle[0]] = color
            # Star left
            if new_particle[0] - 1 >= 0 and new_particle[0] - 1 < self.cols:
                color = blend_colors(
                    new_data[new_particle[1]][new_particle[0] - 1],
                    self.particle_color, particle_strength / 3,
                )
                new_data[new_particle[1]][new_particle[0] - 1] = color
            # Star right
            if new_particle[0] + 1 >= 0 and new_particle[0] + 1 < self.cols:
                color = blend_colors(
                    new_data[new_particle[1]][new_particle[0] + 1],
                    self.particle_color, particle_strength / 3,
                )
                new_data[new_particle[1]][new_particle[0] + 1] = color

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

def scalar_multiplier(vector, scalar):
    '''
    Multiply tuple by scalar value
    '''
    return tuple([scalar * x for x in vector])
