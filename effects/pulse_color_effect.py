'''
Pulse color effect
'''

from colorable_effect_base import ColorableEffectBase

class PulseColorEffect(ColorableEffectBase):
    '''
    Pulse color effect
    '''
    def __init__(self, rows, cols, speed=0.1, points=[(0.0, 0.0), (0.42, 0.0), (0.58, 1.0), (1.0, 1.0)], color=(255, 255, 255)):
        super().__init__(rows, cols)

        self.color = color
        self.time = 0.0
        self.speed = speed
        self.points = points
        self.bezier = points[0][1]

    def evolve(self):
        '''
        Progress 1 speed unit along bezier curve
        '''
        self.time = (self.time + self.speed) % 2.0
        # https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Cubic_B%C3%A9zier_curves
        time = abs(1.0 - self.time)
        time_diff = 1.0 - time
        term1 = scalar_multiplier(self.points[0], time_diff ** 3)
        term2 = scalar_multiplier(self.points[1], 3 * time_diff ** 2 * time)
        term3 = scalar_multiplier(self.points[2], 3 * time_diff * time ** 2)
        term4 = scalar_multiplier(self.points[3], time ** 3)
        self.bezier = term1[1] + term2[1] + term3[1] + term4[1]

    def get_pixel(self, x_coord, y_coord):
        return (self.color[0] * self.bezier, self.color[1] * self.bezier, self.color[2] * self.bezier)

def scalar_multiplier(vector, scalar):
    '''
    Multiply tuple by scalar value
    '''
    return tuple([scalar * x for x in vector])
