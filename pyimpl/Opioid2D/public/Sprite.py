"""Sprites and SpriteGroups
"""

__all__ = [
    "Sprite",
    "SpriteGroup",
    "SpritePool",
    ]

import cOpioid2D as _c
from Opioid2D.public.Node import Node
from Opioid2D.public.Director import Director
from Opioid2D.public.ResourceManager import ResourceManager
from Opioid2D.internal.objectmgr import ObjectManager
from Opioid2D.internal.gridimage import GridImage
from Opioid2D.public.Image import Image, ImageInstance
from Opioid2D.public.Bitmap import Bitmap

import sys, pygame

class SpriteMeta(type):
    def __init__(self, name, bases, dct):
        type.__init__(self, name, bases, dct)
        self._init_image = dct.get("image") or self._init_image
        self._init_layer = dct.get("layer") or self._init_layer
        self.image = property(self.get_image, self.set_image)
        self.layer = property(self.get_layer, self.set_layer)

class Sprite(Node):
    """The Sprite is a Node that has a graphical presentation
    
    The usual way to use Sprites is to subclass the Sprite class
    and set the following class attributes:
        
    group - name of the SpriteGroup that instances of your sprite are automatically added to (can also be a list of names)
    image - name of the imagefile that is loaded for all instances
    layer - name of the layer that the instance is automatically placed on creation
    lighting - boolean setting for automatically enabling or disabling lighting for instances
    
    """
    __metaclass__ = SpriteMeta


    _init_image = None
    _init_layer = None

    group = None

    lighting = False
    
    def __new__(cls, *arg, **kw):
        obj = SpritePool.get_object()
        obj.__class__ = cls
        return obj

    def __init__(self, img=None):
        """Create a Sprite that uses the given image
        
        The image given can be an Image object or a string containing
        the image filename.
        """
        self._preinit(img)
        self.on_create()
        
    def _preinit(self, img):
        if img is None:
            img = self._init_image
        if not hasattr(self, "_cObj") or self._cObj is None:
            self._cObj = _c.Sprite()
        self.set_image(img)

        self._init()
        self._get_physics()
        
        group = self.group
        if group is not None:
            if type(group) not in (list, tuple):
                group = (group,)
            for g in group:
                self.join_group(g)
        if self._init_layer is not None:
            self.set_layer(self._init_layer)
        self.enable_lighting(self.lighting)
        
    def delete(self):
        if self.deleted:
            return
        self.on_delete()
        Node.delete(self)

    def on_create(self):
        """Callback that is invoked when the Sprite object is created.
        
        Override in subclasses"""
        pass
    
    def on_delete(self):
        """Callback that is invoked when the Sprite object is deleted.
        
        Override in subclasses"""
        pass

    def join_group(self, name):
        """Join a new sprite group"""
        scene = Director.scene
        group = scene.get_group(name)
        self._cObj.JoinGroup(group._cObj)

    def leave_group(self, name):
        """Leave a sprite group"""
        scene = Director.scene
        grp = scene.get_group(name)
        self._cObj.LeaveGroup(grp._cObj)

    def enable_lighting(self, flag):
        """Enable or disable lighting for this sprite"""
        self._cObj.EnableLighting(flag)

    def set_color(self, rgba):
        if len(rgba) == 3:
            rgba = rgba + (1,)
        self._cObj.GetColor().set(*rgba)
    def get_color(self):
        c = self._cObj.GetColor()
        return (c.red, c.green, c.blue, c.alpha)
    color = property(get_color, set_color, doc="Color of the sprite in (r,g,b,a)")

    def set_alpha(self, alpha):
        self._cObj.GetColor().alpha = alpha
    def get_alpha(self):
        return self._cObj.GetColor().alpha
    alpha = property(get_alpha, set_alpha, doc="Alpha value of the sprite")

    def set_image(self, image):
        if image is None:
            self._cObj.SetImage(None)
            return
        if isinstance(image, Bitmap):
            image = ResourceManager._create_image(image)
        elif isinstance(image, pygame.Surface):
            image = ResourceManager._create_image(Bitmap(image))
        elif not isinstance(image, ImageInstance):
            image = ResourceManager.get_image(image)        
        self._image = image
        self._cObj.SetImage(image._cObj)
    def get_image(self):
        return self._image
    #current_image = property(get_image, set_image)
    
    def get_hotspot(self):
        if self._image is None:
            return 0,0
        h = self._image.hotspot
        return h.x,h.y
    def set_hotspot(self, (x,y)):
        if self._image is None:
            return
        img = ResourceManager.get_image(self._image, hotspot=(x,y))
        self.image = img
    hotspot = property(get_hotspot, set_hotspot)

    def __del__(self):
        if SpritePool is not None:
            SpritePool.unallocate(self)
            
    def _get_rect(self):
        x,y = self.position
        if self._image is None:
            w,h = 0,0
        else:
            w,h = self._image.size
        sx,sy = self.scale
        w *= sx
        h *= sy
        hs = self._image._cObj.hotspot
        hx,hy = hs.x*w,hs.y*h
        x -= hx
        y -= hy
        return pygame.Rect(x,y,w,h)
    
    def get_rect(self):
        return SpriteRect(self)
    rect = property(get_rect)
    
class SpriteRect(object):
    def __init__(self, sprite):
        self._sprite = sprite
        
    def __getattr__(self, name):
        r = self._sprite._get_rect()
        return getattr(r, name)
    
    def __setattr__(self, name, value):
        if name.startswith("_"):
            return object.__setattr__(self, name, value)
        r1 = self._sprite._get_rect()
        r2 = pygame.Rect(r1)
        setattr(r2, name, value)
        dx = r2.left - r1.left
        dy = r2.top - r1.top
        self._sprite.position += (dx,dy)

class SpriteGroup(object):
    """SpriteGroups are logical groups for sprites used for controlling collisions and other behavior.
    """
    def __init__(self, cobj):
        self._cObj = cobj
        self.mutators = set()
        
    def add_mutator(self, mutator):
        self._cObj.AddMutator(mutator)
        self.mutators.add(mutator)
        
    def do(self, act):
        for s in self:
            s.do(act)
        
    def __iter__(self):
        v = self._cObj.ListSprites()
        l = (ObjectManager.c2py(obj) for obj in v)
        return l
    
    def __len__(self):
        return self._cObj.GetSize()
    
    def pick(self, x, y):
        sprite = self._cObj.Pick(_c.Vec2(x,y))
        return ObjectManager.c2py(sprite)


class SpritePool(object):
    """Utility for pre-creating sprite objects
    """

    def __init__(self):
        self.clearing = False
        self.clear()

    def preallocate(self, num):
        self.cache.extend(object.__new__(Sprite) for i in range(num))

    def clear(self):
        self.clearing = True
        self.cache = []
        self.used = 0
        self.clearing = False

    def unallocate(self, obj):
        if self.clearing:
            return
        self.clearing = True
        cObj = obj._cObj
        obj.__dict__.clear()
        cObj.ReUse()
        obj._cObj = cObj
        self.clearing = False
        if self.used == 0:
            self.cache.append(obj)
        else:
            self.used -= 1
            self.cache[self.used] = obj

    def get_object(self):
        if self.used == len(self.cache):
            #self.cache.append(object.__new__(Sprite))
            return object.__new__(Sprite)
        obj = self.cache[self.used]
        self.cache[self.used] = None
        self.used += 1
        return obj

    def get(self, cls, *arg, **kw):
        obj = self.get_object()
        obj.__class__ = cls
        obj.__init__(*arg, **kw)
        return obj

    def __del__(self):
        self.clearing = True
        self.clear()
            
SpritePool = SpritePool()
