'''
Solid color effect
'''

from colorable_effect_base import ColorableEffectBase

class SolidColorEffect(ColorableEffectBase): # pylint: disable=too-few-public-methods
    '''
    Solid color effect
    '''
    def __init__(self, rows, cols, color=(255, 255, 255)):
        super().__init__(rows, cols)

        self.color = color

    def get_pixel(self, x_coord, y_coord):
        return self.color
