import math
import random
import time
from opc_imp import color_utils


class Throbber(object):
    def __init__(self, display_element, rate_scale = .1):
        self.__speeds = { 'r': 6, 'g': -7, 'b': 11 }
        self.__background_hum = { 'r': 20, 'g': 24, 'b': 22 }
        self.__display_element = display_element
        self.__start_time = time.time()
        self.__rate_scale = rate_scale

    def __calc_a_color(self, tick, pixel, cname):
        n_pixels = self.__display_element.length
        center_px = (tick / self.__speeds[cname]) % n_pixels
        rads = ((center_px + pixel) % n_pixels) / float(n_pixels) * math.pi * 2
        cv = math.cos(rads)
        band_mult = math.cos(tick * self.__background_hum[cname])
        v = color_utils.remap((cv * band_mult), -1, 1, 0, 10)
        return v

    def tick(self):
        t = (time.time() - self.__start_time) * self.__rate_scale
        for pinx in range(self.__display_element.length):
            r = self.__calc_a_color(t, pinx, 'r')
            g = self.__calc_a_color(t, pinx, 'g')
            b = self.__calc_a_color(t, pinx, 'b')
            self.__display_element.set_pixel(pinx, (r,g,b))
