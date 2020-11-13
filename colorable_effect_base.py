'''
Colorable Effect Class
'''

from effect_base import EffectBase

class ColorableEffectBase(EffectBase):
    '''
    Colorable Effect Base
    '''
    def __init__(self, rows, cols):
        super().__init__(rows, cols)

        self.color = (255, 255, 255)

    def change_color(self, new_color):
        self.color = new_color
