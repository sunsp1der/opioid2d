
__all__ = [
    "Image",
    ]

import os

class ImageMeta(type):
    subclasses = set()
    
    def __init__(cls, name, bases, dct):
        type.__init__(cls, name, bases, dct)
        if cls.filename is not None:
            ImageMeta.subclasses.add(self)
            self.filename = self.filename.replace(os.path.sep, "/")
            
class Image(object):
    filename = None
    hotspot = (0.5, 0.5)
    mode = []
    preload = False
    border = 1
    collision = []

    __metaclass__ = ImageMeta

#    def __init__(self):
#        self._cObj = None

    def _get_key(self):
        return (self.filename, self.hotspot, tuple(self.mode), self.border, tuple(self.collision))

    def __cmp__(self, other):
        return cmp(self._get_key(), other._get_key())

    def __hash__(self):
        return hash(self._get_key())

    def __eq__(self, other):
        return self._get_key() == other._get_key()

    def __repr__(self):
        return str(self._get_key())
    
    def copy(self):
        obj = object.__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj
    
class ImageInstance(object):
    def __init__(self, cobj, imgkey=None):
        self._cObj = cobj
        self._key = imgkey
        
    def transform(self, mode):
        from Opioid2D.public.ResourceManager import ResourceManager
        k = self._key
        if mode not in k.mode:
            return ResourceManager.get_image(k, mode=k.mode+[mode])
        return self
    
    def get_width(self):
        return self._cObj.w
    width = property(get_width)
    
    def get_height(self):
        return self._cObj.h
    height = property(get_height)
    
    def get_size(self):
        c = self._cObj
        return c.w,c.h
    size = property(get_size)

    def add_collision_node(self, x, y, w, h):
        self._cObj.AddCollisionNode(x,y,w,h)

