'''
Neopixel Simulator Output Class
'''
import pygame
from output_base import OutputBase

class SimulatorOutput(OutputBase): # pylint: disable=too-few-public-methods
    '''
    Simulator output
    '''

    PIXEL_SIZE = 20
    BUFFER = 10

    def __init__(self, rows = 6, cols = 50):
        self.rows = rows
        self.cols = cols

        pygame.init()
        self.window = pygame.display.set_mode((
            self.cols * self.PIXEL_SIZE + 2 * self.BUFFER,
            self.rows * self.PIXEL_SIZE + 2 * self.BUFFER
        ))
        pygame.display.set_caption('Neopixel Simulator')

    def write(self, data):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        for x_coord in range (0, self.cols):
            for y_coord in range (0, self.rows):
                pygame.draw.rect(self.window, data[y_coord][x_coord],
                    [
                        self.BUFFER + (x_coord * self.PIXEL_SIZE),
                        self.BUFFER + (y_coord * self.PIXEL_SIZE),
                        20, 20
                    ]
                )

        pygame.display.update()

        return True
