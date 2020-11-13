import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 300, brightness=0.2)

for i in range(0,100):
    pixels[i] = 0xD70270
for i in range(100,200):
    pixels[i] = 0x734F96
for i in range(200,300):
    pixels[i] = 0x0038A8
