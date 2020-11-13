# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)

while True:
    for i in range(0, num_pixels):
        # for j in range(4):
        #     bratio = abs(5-j) / 5
        #     pixels.fill((0,0,0))
        #     pixels[i] = (255 * bratio, 255 * bratio, 255 * bratio)
        #     pixels.show()
        #     time.sleep(0.001)
        pixels.fill((0,0,0))
        pixels[i] = (255, 255, 255)
        pixels[(i - 1) % num_pixels] = (50, 50, 50)
        pixels[(i + 1) % num_pixels] = (50, 50, 50)
        pixels[(i + 2) % num_pixels] = (10, 10, 10)
        pixels[(i - 2) % num_pixels] = (10, 10, 10)
        pixels.show()
        time.sleep(0.005)

