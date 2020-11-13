'''
Lil test script
'''

import time
import pygame

ROWS = 10
COLS = 15
BUFFER = 10
PIXEL_SIZE = 20

pygame.init()
gameDisplay = pygame.display.set_mode(
    (COLS * PIXEL_SIZE + 2 * BUFFER, ROWS * PIXEL_SIZE + 2 * BUFFER)
)
pygame.display.set_caption('Neopixel Simulator')

CRASHED = False

i = 0

while not CRASHED:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            CRASHED = True

    for x in range (0, COLS):
        for y in range (0, ROWS):
            pygame.draw.rect(gameDisplay, 
            ((x * 10 * i) % 255, (y * 10 * i) % 255, ((x+y) * i * 10) % 255),
            [BUFFER + (x * PIXEL_SIZE), BUFFER + (y * PIXEL_SIZE), 20, 20])

    pygame.display.update()

    i += 1
    time.sleep(0.01)

pygame.quit()
