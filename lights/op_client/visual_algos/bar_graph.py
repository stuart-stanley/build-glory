import time

class BarGrapher(object):
    def __init__(self, display_element, data_cb, data_max=None, rate=0.5):
        self.__display_element = display_element
        self.__data_cb = data_cb
        self.__rate = 1.0 / rate  # in updates per second
        self.__last_update = time.time() - rate
        nxp = display_element.length
        if data_max is None:
            data_max = (nxp, nxp, nxp)

        assert len(data_max) == 3, 'must be color-like-tuple of 3'

        self.__data_scale = []
        for colors_max in data_max:
            self.__data_scale.append(colors_max / float(nxp))


    def __figure_color(self, pinx, scaled_size):
        if pinx < scaled_size:
            c = int((64.0 / scaled_size) * pinx)
        else:
            c = 0
        return c

    def tick(self):
        dt = time.time() - self.__last_update
        if dt < self.__rate:
            return
        self.__last_update += self.__rate

        unscaled_colors = self.__data_cb()
        assert len(unscaled_colors) == 3, \
            'data-callback {} return {}, which was not a 3 item list'.format(
                self.__data_cb, unscaled_colors)
        n_pixels = self.__display_element.length
        scaled_sizes = []
        for inx in range(len(self.__data_scale)):
             scaled_size = unscaled_colors[inx] * self.__data_scale[inx]
             scaled_sizes.append(scaled_size)

        for pinx in range(n_pixels):
            r = self.__figure_color(pinx, scaled_sizes[0])
            g = self.__figure_color(pinx, scaled_sizes[1])
            b = self.__figure_color(pinx, scaled_sizes[2])
            self.__display_element.set_pixel(pinx, (r,g,b))

