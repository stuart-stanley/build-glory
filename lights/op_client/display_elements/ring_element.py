from base_element import BaseDisplayElement


class RingDisplayElement(BaseDisplayElement):
    def __init__(self, name, properties):
        self._validate_properties(properties, ["length"])
        start = properties["start"]
        length = properties["length"]
        super(RingDisplayElement, self).__init__('ring', name, start, length)
