import json
import copy
from display_elements import element_factory, RawDisplayElement

class LayoutHandler(object):
    def __init__(self, layout_file_name):
        with open(layout_file_name, 'r') as layout_file:
            jdata = json.load(layout_file)

        pixels = []
        displays = None
        for layout_item in jdata:
            if "point" in layout_item:
                pixels.append(layout_item)
            elif "displays" in layout_item:
                assert displays is None, "multiple displays items"
                displays = layout_item["displays"]

        disp_objs = {}
        if displays is not None:
            for dname, ddata in displays.items():
                disp_objs[dname] = element_factory(dname, ddata)

        assert "raw" not in disp_objs, \
            "reserved display element name 'raw' was used"
        disp_objs['raw'] = RawDisplayElement('raw', properties = { "start": 0, "width": len(pixels) })
        self.__display_elements = disp_objs

        self.__figure_start_ordered()
        self.__last_pixels = None

    def __figure_start_ordered(self):
        dec = copy.copy(self.__display_elements)
        del dec['raw']
        ordered_elements = []
        next_min_better_be = 0
        while len(dec) > 0:
            min_de = None
            print "---->", len(dec)
            for de in dec.values():
                print "  ", de.name, de.start
                if min_de is None:
                    print "None"
                else:
                    print min_de.name, min_de.start
                if min_de is None or de.start < min_de.start:
                    min_de = de

            assert next_min_better_be == min_de.start, \
                "Element '{}' started at {}, but should have been at {}".format(
                    min_de.name, min_de.start, next_min_better_be)
            print "======", min_de.name, min_de.start
            next_min_better_be = min_de.start + min_de.length
            ordered_elements.append(min_de)
            del dec[min_de.name]
        self.__ordered_elements = ordered_elements

    def __check_element(self, element_name, element_type):
        assert element_name in self.__display_elements, \
            "Element '{}' is not defined in {} -> {}".format(
                element_name, self.__layout_file_name, self.__display_elements.keys())

        element = self.__display_elements[element_name]
        assert element.element_type == element_type, \
            "Element '{}' is a {} not the requested type {}".format(
                element_name, element.element_type, element_type)
        return element

    def get_strand_element(self, element_name):
        element = self.__check_element(element_name, 'strand')
        return element

    def get_banner_element(self, element_name):
        element = self.__check_element(element_name, 'banner')
        return element

    def get_conrings_element(self, element_name):
        element = self.__check_element(element_name, 'concentric_rings')
        return element

    def get_raw_space(self):
        element = self.__check_element('raw', 'strand')
        return element
        

    def render(self, opc_client):
        send_pixels = [(0,0,0)]  # gl_server bug??!?!?
        send_pixels = []
        for de in self.__ordered_elements:
            send_pixels.extend(de.pixel_buffer)
        opc_client.put_pixels(send_pixels)
        #if self.__last_pixels is not None:
        #    dcnt = 0
        #    for inx in range(len(send_pixels)):
        #        if send_pixels[inx] != self.__last_pixels[inx]:
        #            dcnt += 1
        #    print "delta", dcnt
        #self.__last_pixels = send_pixels
                             




if __name__ == '__main__':
    ly = LayoutHandler('../openpixelcontrol/layouts/concircs.json')

