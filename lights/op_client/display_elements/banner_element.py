import math
import copy
import time
from base_element import BaseDisplayElement

# Digit value to bitmask mapping:
# (note: snagged from https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/AlphaNum4.py)
_DIGIT_VALUES = {
' ' : [0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000],
'!' : [0b01011111, 0b00000000, 0b00000000, 0b00000000, 0b00000000],
'"' : [0b00000011, 0b00000000, 0b00000011, 0b00000000, 0b00000000],
'#' : [0b00010100, 0b00111110, 0b00010100, 0b00111110, 0b00010100],
'$' : [0b00100100, 0b01101010, 0b00101011, 0b00010010, 0b00000000],
'%' : [0b01100011, 0b00010011, 0b00001000, 0b01100100, 0b01100011],
'&' : [0b00110110, 0b01001001, 0b01010110, 0b00100000, 0b01010000],
'\'' : [0b00000011, 0b00000000, 0b00000000, 0b00000000, 0b00000000],
'(' : [0b00011100, 0b00100010, 0b01000001, 0b00000000, 0b00000000],
')' : [0b01000001, 0b00100010, 0b00011100, 0b00000000, 0b00000000],
'*' : [0b00101000, 0b00011000, 0b00001110, 0b00011000, 0b00101000],
'+' : [0b00001000, 0b00001000, 0b00111110, 0b00001000, 0b00001000],
',' : [0b10110000, 0b01110000, 0b00000000, 0b00000000, 0b00000000],
'-' : [0b00001000, 0b00001000, 0b00001000, 0b00001000, 0b00000000],
'.' : [0b01100000, 0b01100000, 0b00000000, 0b00000000, 0b00000000],
'/' : [0b01100000, 0b00011000, 0b00000110, 0b00000001, 0b00000000],
'0' : [0b00111110, 0b01000001, 0b01000001, 0b00111110, 0b00000000],
'1' : [0b01000010, 0b01111111, 0b01000000, 0b00000000, 0b00000000],
'2' : [0b01100010, 0b01010001, 0b01001001, 0b01000110, 0b00000000],
'3' : [0b00100010, 0b01000001, 0b01001001, 0b00110110, 0b00000000],
'4' : [0b00011000, 0b00010100, 0b00010010, 0b01111111, 0b00000000],
'5' : [0b00100111, 0b01000101, 0b01000101, 0b00111001, 0b00000000],
'6' : [0b00111110, 0b01001001, 0b01001001, 0b00110000, 0b00000000],
'7' : [0b01100001, 0b00010001, 0b00001001, 0b00000111, 0b00000000],
'8' : [0b00110110, 0b01001001, 0b01001001, 0b00110110, 0b00000000],
'9' : [0b00000110, 0b01001001, 0b01001001, 0b00111110, 0b00000000],
':' : [0b01010000, 0b00000000, 0b00000000, 0b00000000, 0b00000000],
';' : [0b10000000, 0b01010000, 0b00000000, 0b00000000, 0b00000000],
'<' : [0b00010000, 0b00101000, 0b01000100, 0b00000000, 0b00000000],
'=' : [0b00010100, 0b00010100, 0b00010100, 0b00000000, 0b00000000],
'>' : [0b01000100, 0b00101000, 0b00010000, 0b00000000, 0b00000000],
'?' : [0b00000010, 0b01011001, 0b00001001, 0b00000110, 0b00000000],
'@' : [0b00111110, 0b01001001, 0b01010101, 0b01011101, 0b00001110],
'A' : [0b01111110, 0b00010001, 0b00010001, 0b01111110, 0b00000000],
'B' : [0b01111111, 0b01001001, 0b01001001, 0b00110110, 0b00000000],
'C' : [0b00111110, 0b01000001, 0b01000001, 0b00100010, 0b00000000],
'D' : [0b01111111, 0b01000001, 0b01000001, 0b00111110, 0b00000000],
'E' : [0b01111111, 0b01001001, 0b01001001, 0b01000001, 0b00000000],
'F' : [0b01111111, 0b00001001, 0b00001001, 0b00000001, 0b00000000],
'G' : [0b00111110, 0b01000001, 0b01001001, 0b01111010, 0b00000000],
'H' : [0b01111111, 0b00001000, 0b00001000, 0b01111111, 0b00000000],
'I' : [0b01000001, 0b01111111, 0b01000001, 0b00000000, 0b00000000],
'J' : [0b00110000, 0b01000000, 0b01000001, 0b00111111, 0b00000000],
'K' : [0b01111111, 0b00001000, 0b00010100, 0b01100011, 0b00000000],
'L' : [0b01111111, 0b01000000, 0b01000000, 0b01000000, 0b00000000],
'M' : [0b01111111, 0b00000010, 0b00001100, 0b00000010, 0b01111111],
'N' : [0b01111111, 0b00000100, 0b00001000, 0b00010000, 0b01111111],
'O' : [0b00111110, 0b01000001, 0b01000001, 0b00111110, 0b00000000],
'P' : [0b01111111, 0b00001001, 0b00001001, 0b00000110, 0b00000000],
'Q' : [0b00111110, 0b01000001, 0b01000001, 0b10111110, 0b00000000],
'R' : [0b01111111, 0b00001001, 0b00001001, 0b01110110, 0b00000000],
'S' : [0b01000110, 0b01001001, 0b01001001, 0b00110010, 0b00000000],
'T' : [0b00000001, 0b00000001, 0b01111111, 0b00000001, 0b00000001],
'U' : [0b00111111, 0b01000000, 0b01000000, 0b00111111, 0b00000000],
'V' : [0b00001111, 0b00110000, 0b01000000, 0b00110000, 0b00001111],
'W' : [0b00111111, 0b01000000, 0b00111000, 0b01000000, 0b00111111],
'X' : [0b01100011, 0b00010100, 0b00001000, 0b00010100, 0b01100011],
'Y' : [0b00000111, 0b00001000, 0b01110000, 0b00001000, 0b00000111],
'Z' : [0b01100001, 0b01010001, 0b01001001, 0b01000111, 0b00000000],
'[' : [0b01111111, 0b01000001, 0b00000000, 0b00000000, 0b00000000],
'\\' : [0b00000001, 0b00000110, 0b00011000, 0b01100000, 0b00000000],
']' : [0b01000001, 0b01111111, 0b00000000, 0b00000000, 0b00000000],
'^' : [0b00000010, 0b00000001, 0b00000010, 0b00000000, 0b00000000],
'-' : [0b01000000, 0b01000000, 0b01000000, 0b01000000, 0b00000000],
'`' : [0b00000001, 0b00000010, 0b00000000, 0b00000000, 0b00000000],
'a' : [0b00100000, 0b01010100, 0b01010100, 0b01111000, 0b00000000],
'b' : [0b01111111, 0b01000100, 0b01000100, 0b00111000, 0b00000000],
'c' : [0b00111000, 0b01000100, 0b01000100, 0b00101000, 0b00000000],
'd' : [0b00111000, 0b01000100, 0b01000100, 0b01111111, 0b00000000],
'e' : [0b00111000, 0b01010100, 0b01010100, 0b00011000, 0b00000000],
'f' : [0b00000100, 0b01111110, 0b00000101, 0b00000000, 0b00000000],
'g' : [0b10011000, 0b10100100, 0b10100100, 0b01111000, 0b00000000],
'h' : [0b01111111, 0b00000100, 0b00000100, 0b01111000, 0b00000000],
'i' : [0b01000100, 0b01111101, 0b01000000, 0b00000000, 0b00000000],
'j' : [0b01000000, 0b10000000, 0b10000100, 0b01111101, 0b00000000],
'k' : [0b01111111, 0b00010000, 0b00101000, 0b01000100, 0b00000000],
'l' : [0b01000001, 0b01111111, 0b01000000, 0b00000000, 0b00000000],
'm' : [0b01111100, 0b00000100, 0b01111100, 0b00000100, 0b01111000],
'n' : [0b01111100, 0b00000100, 0b00000100, 0b01111000, 0b00000000],
'o' : [0b00111000, 0b01000100, 0b01000100, 0b00111000, 0b00000000],
'p' : [0b11111100, 0b00100100, 0b00100100, 0b00011000, 0b00000000],
'q' : [0b00011000, 0b00100100, 0b00100100, 0b11111100, 0b00000000],
'r' : [0b01111100, 0b00001000, 0b00000100, 0b00000100, 0b00000000],
's' : [0b01001000, 0b01010100, 0b01010100, 0b00100100, 0b00000000],
't' : [0b00000100, 0b00111111, 0b01000100, 0b00000000, 0b00000000],
'u' : [0b00111100, 0b01000000, 0b01000000, 0b01111100, 0b00000000],
'v' : [0b00011100, 0b00100000, 0b01000000, 0b00100000, 0b00011100],
'w' : [0b00111100, 0b01000000, 0b00111100, 0b01000000, 0b00111100],
'x' : [0b01000100, 0b00101000, 0b00010000, 0b00101000, 0b01000100],
'y' : [0b10011100, 0b10100000, 0b10100000, 0b01111100, 0b00000000],
'z' : [0b01100100, 0b01010100, 0b01001100, 0b00000000, 0b00000000],
'{' : [0b00001000, 0b00110110, 0b01000001, 0b00000000, 0b00000000],
'|' : [0b01111111, 0b00000000, 0b00000000, 0b00000000, 0b00000000],
'}' : [0b01000001, 0b00110110, 0b00001000, 0b00000000, 0b00000000],
'~' : [0b00001000, 0b00000100, 0b00001000, 0b00000100, 0b00000000],
None: [0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111]
}


class BannerDisplayElement(BaseDisplayElement):
    def __init__(self, name, properties):
        self._validate_properties(properties, ["width", "height"])
        start = properties["start"]
        self.width = properties["width"]
        self.height = properties["height"]
        self.font_width = 6
        self.text_length = int(math.ceil(self.width / 6.0))

        length = self.width * self.height
        super(BannerDisplayElement, self).__init__('banner', name, start, length)

    def set_xy_pixel(self, x, y, color, allow_oob=False):
        if x < 0 or x >= self.width or y < 0 or y>= self.height:
            assert allow_oob, \
                'Attempt to write location {},{} outside 0..{}, 0..{}'.format(
                    x, y, self.width, self.height)
            # outside of display. Just ignore
            return
        inx = self.height * x
        #print "inx=", inx,
        if x % 2 == 0:
            #print "add-even", y,
            inx += y
        else:
            #print "add-odd", self.height, y, self.height - y,
            inx += (self.height - y - 1)

        #print "final_inx", inx, color
        self.set_pixel(inx, color)

    def set_char(self, char, col_num, row_num=0, color=None, background=None):
        if char not in _DIGIT_VALUES:
            bits = copy.copy(_DIGIT_VALUES[None])
        else:
            bits = copy.copy(_DIGIT_VALUES[char])
        if color is None:
            color = (255, 255, 255)
        if background is None:
            background = (0,0,0)
        bits.append(0b00000000)

        for col_offset in range(0, len(bits)):
            col = col_num + col_offset
            cdata = bits[col_offset]
            #print "col", col_offset, col, cdata
            for row_offset in range(0, 8):
                row = row_num + row_offset
                rmask = 1 << row_offset
                if rmask & cdata > 0:
                    use_color = color
                else:
                    use_color = background
                #print "  row", col, row_offset, row, rmask, use_color,
                self.set_xy_pixel(col, row, use_color, allow_oob=True)

    def scroll_text(self, color=None):
        sc = (0 - self.__scroll_inx) / self.font_width
        if sc >= len(self.__scroll_text):
            sc = 0
            self.__scroll_inx = 0
        our_text = self.__scroll_text[sc:sc + self.text_length]
        #print sc, sc + self.text_length,
        #print "--{}--".format(our_text)
        start_col = 0 - (abs(self.__scroll_inx) % self.font_width)
        for send_index in range(0, self.font_width):
            if send_index >= len(our_text):
                cts = ' '
            else:
                cts = our_text[send_index]
            self.set_char(cts, start_col, color=color)
            start_col += self.text_length
        self.__scroll_inx -= 1

    def tick(self, color=None):
        ct = time.time()
        lst = ct - self.__last_scroll
        scount = 0
        while lst > self.__scroll_rate:
            self.scroll_text(color=color)
            scount += 1
            self.__last_scroll += self.__scroll_rate
            lst = ct - self.__last_scroll

        # if scount > 1:
        #     print "WARNING: had to jump scroll {} {}s intervals".format(
        #         scount, self.__scroll_rate)


    def set_scroll_text(self, text, scroll_rate=10):
        self.__scroll_rate = 1.0 / scroll_rate
        self.__start_time = time.time() - self.__scroll_rate
        self.__last_scroll = self.__start_time
        pad = ' ' * self.font_width
        self.__scroll_text = pad + text
        self.__scroll_inx = 0




