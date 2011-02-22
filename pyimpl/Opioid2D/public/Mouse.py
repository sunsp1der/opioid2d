
__all__ = [
    "Mouse",
    "HWCursor",
    ]

import pygame.mouse as mouse
import pygame.cursors as cursors

from Opioid2D.public.Sprite import Sprite


class Mouse(object):
    def __init__(self):
        self._mscalex = 1.0
        self._mscaley = 1.0
        self._cursor = None
        self._sprite = None
    
    def get_position(self):
        mx,my = mouse.get_pos()
        return mx*self._mscalex, my*self._mscaley
    def set_position(self,(x,y)):
        mouse.set_pos((x/self._mscalex,y/self._mscaley))
    position = property(get_position, set_position)

    def get_world_position(self, layer):
        return layer.convert_pos(self.get_position)

    def get_cursor(self):
        return self._cursor
    def set_cursor(self, cursor):
        """cursor can be either None, image name, Image, Sprite or HWCursor)"""
        if cursor is None:
            mouse.set_visible(False)
            self._sprite = None
            self._cursor = None
        elif isinstance(cursor, HWCursor):
            self._cursor = cursor
            self._sprite = None
            mouse.set_cursor(*cursor._data)
            mouse.set_visible(True)
        elif isinstance(cursor, Sprite):
            mouse.set_visible(False)
            self._sprite = cursor
            self._cursor = self.sprite
        else:
            s = Sprite(cursor)
            mouse.set_visible(False)
            self._sprite = s
            self._cursor = s
            
    cursor = property(get_cursor, set_cursor)
Mouse = Mouse()

_default_pygame_cursors = [
    "arrow",
    "diamond",
    "broken_x",
    "tri_left",
    "tri_right",
    ]

class HWCursor(object):

    @classmethod
    def compile(cls, strings, black='X', white='.', xor='o', hotspot=(0,0)):
        size = len(strings[0]), len(strings)
        data,mask = cursors.compile(strings, black, white, xor)
        hwc = HWCursor()
        hwc._data = size, hotspot, data, mask
        return hwc

    @classmethod
    def from_pygame(cls, pygame_cursor):
        hwc = HWCursor()
        hwc._data = pygame_cursor
        return hwc

    def get_size(self):
        return self._data[0]
    size = property(get_size)

    def get_hotspot(self):
        return self._data[1]
    hotspot = property(get_hotspot)


for _c in _default_pygame_cursors:
    setattr(HWCursor, _c, HWCursor.from_pygame(getattr(cursors, _c)))

Mouse._cursor = HWCursor.arrow

