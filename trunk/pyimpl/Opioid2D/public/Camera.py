
__all__ = [
    "Camera"
    ]

import cOpioid2D as _c
from Opioid2D.internal.objectmgr import ObjectManager
from Opioid2D.public.Node import NodeBase

class Camera(NodeBase):
    def __init__(self, cobj):
        self._cObj = cobj
        self._physics = None
        self._actions = set()
        self.deleted = False

    def __getitem__(self, i):
        return self.position[i]
    
    def get_align(self):
        return self._cObj.GetAlign()
    def set_align(self, flag):
        self._cObj.SetAlign(flag)
    align = property(get_align, set_align)
