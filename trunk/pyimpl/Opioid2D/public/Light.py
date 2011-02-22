
__all__ = [
    "Light",
    ]

import cOpioid2D as _c
from Opioid2D.internal.objectmgr import ObjectManager

class Light(object):
    def __init__(self):
        self._cObj = _c.Light()
        ObjectManager.register(self)

    def _on_mgr_delete(self):
        pass

    def set_color(self, r,g,b):
        self._cObj.color.set(r,g,b)

    def set_intensity(self, i):
        self._cObj.intensity = i

    def set_cutoff(self, co):
        self._cObj.cutoff = co

    def set_pos(self, x, y):
        self._cObj.pos.set(x,y)

    def attach_to(self, node):
        self._cObj.node = node._cObj
        self._node = node
