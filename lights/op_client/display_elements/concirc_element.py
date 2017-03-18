from base_element import BaseDisplayElement
from ring_element import RingDisplayElement

class ConcentricCircleDisplayElement(BaseDisplayElement):
    def __init__(self, name, properties):
        self._validate_properties(properties, ["length", "ring_counts"])
        start = properties["start"]
        length = properties["length"]
        super(ConcentricCircleDisplayElement, self).__init__(
            'concentric_rings', name, start, length)

        self.__rings = []
        for ring_count in properties["ring_counts"]:
            ring_props = { 'start': start, 'length': ring_count }
            ring = RingDisplayElement("{}.{}".format(name, ring_count), ring_props)
            self.__rings.append(ring)



