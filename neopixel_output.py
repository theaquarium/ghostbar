'''
Real Neopixel Output Class
'''
import board
import neopixel
from output_base import OutputBase

class PixelInfo: # pylint: disable=too-few-public-methods
    '''
    Neopixel Config Object
    '''
    def __init__(self, pin='D18', order='GRB', brightness=1):
        self.pin = board[pin]
        self.order = neopixel[order]
        self.brightness = brightness

class NeopixelOutput(OutputBase): # pylint: disable=too-few-public-methods
    '''
    Neopixel output
    '''

    def __init__(self, pixel_info=PixelInfo(), rows=6, cols=50, max_amps=15):
        self.rows = rows
        self.cols = cols
        self.max_amps = max_amps
        self.old_data = []

        self.pixels = neopixel.NeoPixel(
            pixel_info.pin, self.rows * self.cols,
            brightness=pixel_info.brightness, auto_write=False, pixel_order=pixel_info.order
        )

    def write(self, data):
        if data != self.old_data:
            # Clear pixels
            self.pixels.fill((0, 0, 0))

            pixel_vals = []
            total_amps = 0.0

            for x_coord in range (0, self.cols):
                reverse = x_coord % 2 == 1
                for y_coord in range (0, self.rows):
                    pixel_num = y_coord * self.cols
                    # If this row runs in reverse, reverse the order
                    if reverse:
                        pixel_num += x_coord
                    else:
                        pixel_num += (self.cols - 1) - x_coord

                    pixel_vals[pixel_num] = data[y_coord][x_coord]
                    for brightness in data[y_coord][x_coord]:
                        total_amps += (brightness / 255) * 0.02 # 0.02A is per-color power draw

            if total_amps > self.max_amps:
                power_scaler = self.max_amps / total_amps
            else:
                power_scaler = 1

            for (pixel_num, pixel_val) in enumerate(pixel_vals):
                self.pixels[pixel_num] = pixel_val * power_scaler

            self.pixels.show()

            self.old_data = data

        return True
