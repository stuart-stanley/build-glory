from base_element import BaseDisplayElement


class StrandDisplayElement(BaseDisplayElement):
    def __init__(self, name, properties):
        self._validate_properties(properties, ["width"])
        start = properties["start"]
        length = properties["width"]
        self.__width = length
        super(StrandDisplayElement, self).__init__('strand', name, start, length)

    def set_pixel(self, inx, color):
        super(StrandDisplayElement, self).set_pixel(inx, color)


class RawDisplayElement(StrandDisplayElement):
    """
    The 'raw' display just treats the whole set of pixels
    as a giant strand.
    """
    pass
