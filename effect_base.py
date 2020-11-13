'''
Generic Effect Class
'''

class EffectBase:
    '''
    Generic Effect Base
    '''
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def evolve(self):
        '''
        Update internal state to new state
        '''

    def get_pixel(self, x_coord, y_coord):
        '''
        Get color at specific pixel
        '''

    def get_data(self, brightness=1):
        '''
        Get full 2D array
        '''
        data = []
        for y_coord in range (0, self.rows):
            data.append([])
            for x_coord in range (0, self.cols):
                col = tuple([brightness * x for x in self.get_pixel(x_coord, y_coord)])
                data[y_coord].append(col)

        return data
