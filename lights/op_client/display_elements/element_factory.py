from strand_element import StrandDisplayElement
from banner_element import BannerDisplayElement
from concirc_element import ConcentricCircleDisplayElement


def element_factory(display_name, properties):
    assert "type" in properties, \
        "required property 'type' missing from {}:{}".format(display_name, properties)
    dtype = properties["type"]
    if dtype == "strip":
        el = StrandDisplayElement(display_name, properties)
    elif dtype == 'banner':
        el = BannerDisplayElement(display_name, properties)
    elif dtype == 'conring':
        el = ConcentricCircleDisplayElement(display_name, properties)
    else:
        assert False, "unknown display-element type '{}'".format(dtype)

    return el
