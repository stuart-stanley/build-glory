

class BaseDisplayElement(object):
    def __init__(self, element_type, name, start, length):
        self.name = name
        self.start = start
        self.length = length
        self.element_type = element_type
        # Start them all as black.
        self.__pixels = [(0,0,0)] * self.length

    @property
    def pixel_buffer(self):
        return self.__pixels

    def _validate_properties(self, properties, more_to_check=None):
        """
        Check that we have everything we need
        """
        check_set = ["start"]
        if more_to_check is not None:
            check_set.extend(more_to_check)
        for check_for in check_set:
            assert check_for in properties, \
                "required property '{}' missing".formnat(check_for)

    def __check_inx_and_color(self, inx, color):
        assert inx < self.length, \
            'Trying to write off end of data. Requested inx={}, length={}'.format(
                inx, self.length)
        # todo, check color.

    def set_pixel(self, inx, color):
        self.__check_inx_and_color(inx, color)
        self.__pixels[inx] = color