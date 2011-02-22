
__all__ = [
    "ParticleSystem",
    
    "PointEmitter",
    ]

from Opioid2D.internal.objectmgr import ObjectManager
from Opioid2D.internal.utils import deprecated
from Opioid2D.public.Director import Director
from Opioid2D.public.ResourceManager import ResourceManager
from Opioid2D.public.Node import Node
import cOpioid2D as _c

import copy


class ParticleSystem(object):
    """ParticleSystem renders particles on the screen
    """
    def __init__(self, layer):
        self._cObj = _c.ParticleSystem()
        ObjectManager.register(self)
        l = Director.scene._cObj.GetLayer(layer)
        if l is None:
            raise ValueError("no layer named %r" % layer)
        self._cObj.Place(l)
        self.mutators = set()
        
    def add_mutator(self, mutator):
        self._cObj.AddMutator(mutator)
        self.mutators.add(mutator)

    def _on_mgr_delete(self):
        pass

def _carg(arg):
    if arg is None:
        return None
    if hasattr(arg, "_cObj"):
        return arg._cObj
    if type(arg) is bool:
        return arg
    if type(arg) in (tuple, list):
        if len(arg) != 2:
            raise TypeError("you must use a two-value sequence for random particle attributes")
        param = _c.RandomParameter(*arg)
    else:
        param = _c.ConstParameter(arg)
    return param

class _Prep(object):
    def __init__(self, tmpl, dict):
        object.__setattr__(self, "_tmpl", tmpl)
        object.__setattr__(self, "_dict", dict)
        
    def __setattr__(self, key ,value):
        arg = _carg(value)
        setattr(self._tmpl, key, arg)
        self._dict[key] = arg

class ParticleEmitterMeta(type):
    def __init__(self, name, bases, dict):
        type.__init__(self, name, bases, dict)
        if self._cImpl is not None:
            self._prep_template()
            
    def __setattr__(self, key, value):
        type.__setattr__(self, key, value)
        if key.startswith("_"):
            return
        self._tmpl_uptodate = False

class ParticleEmitterInstance(object):
    def __init__(self, cobj):
        self._cObj = cobj
        ObjectManager.register(self)        

    def _on_mgr_delete(self):
        pass

class ParticleEmitter(object):
    _cImpl = None
    __metaclass__ = ParticleEmitterMeta
    
    image = None

    direction = 0
    angle = 0
    speed = 0
    acceleration = None
    friction = None
    node_velocity = None

    rotation = 0
    rotation_delta = 0

    offset = None
    advance = None

    align_to_direction = True
    align_to_node = True
    rotate_to_node = False
    
    scale = 1
    scale_delta = 0
    
    color = None
    color_delta = None
    color_target = None

    life = 1.0
    fade_time = 0.0
    fade_delay = None
    fade_in = 0

    num_emits = None
    num_particles = 1
    duration = None
    
    emit_delay = None
    emits_per_sec = 10
    
    @classmethod
    @deprecated
    def Emit(cls, system, position=None):
        cls.emit(system, position)
        
    @classmethod
    def emit(cls, system, position=None):
        node = None
        if isinstance(position, Node):
            node = position
        cls.prepare()
        cobj = cls._cImpl()
        cobj.InitFrom(cls._cTemplate)
        if node is not None:
            cobj.AttachTo(node._cObj)
        else:
            cobj.SetPosition(_c.Vec2(*position))
        cobj.SetSystem(system._cObj)
        pyobj = ParticleEmitterInstance(cobj)
        pyobj._argcache = cls._argcache
        if cls.image is not None:
            image = ResourceManager.get_image(cls.image)
            if image is None:
                raise ValueError("could not load image %r" % imagename)
            pyobj.image = image
            cobj.image = image._cObj
        cobj.Start()
        return pyobj
    
    @classmethod
    @deprecated
    def Prepare(cls):
        cls.prepare()
        
    @classmethod
    def prepare(cls):
        if not cls._tmpl_uptodate:
            cls._prep_template()
            
    @classmethod
    @deprecated
    def Copy(cls):
        return cls.copy()
    
    @classmethod
    def copy(cls):
        d = {}
        d.update(cls.__dict__)
        newcls = ParticleEmitterMeta(cls.__name__, cls.__bases__, d)
        return newcls
                
    @classmethod
    def _prep_template(cls):
        cls._cTemplate = cls._cImpl()
        cls._argcache = {}
        t = _Prep(cls._cTemplate, cls._argcache)
        t.direction = cls.direction
        t.angle = cls.angle
        t.speed = cls.speed
        if cls.acceleration is not None:
            x,y = cls.acceleration
            t.acceleration_x = x
            t.acceleration_y = y
        t.friction = cls.friction
        t.rotation = cls.rotation
        t.rotation_delta = cls.rotation_delta
        if cls.offset is not None:
            x,y  = cls.offset
            t.offset_x = x
            t.offset_y = y
        t.advance = cls.advance
        t.node_velocity = cls.node_velocity
        t.align_to_direction = cls.align_to_direction
        t.align_to_node = cls.align_to_node
        t.rotate_to_node = cls.rotate_to_node
        t.scale = cls.scale
        t.scale_delta = cls.scale_delta
        if cls.color is not None:
            r,g,b,a = cls.color
            t.color_red = r
            t.color_green = g
            t.color_blue = b
            t.color_alpha = a
        if cls.color_delta is not None:
            r,g,b,a = cls.color_delta
            t.color_delta_red = r
            t.color_delta_green = g
            t.color_delta_blue = b
            t.color_delta_alpha = a
        if cls.color_target is not None:
            r,g,b,a = cls.color_target
            t.color_target_red = r
            t.color_target_green = g
            t.color_target_blue = b
            t.color_target_alpha = a
        t.life = cls.life
        t.fade_time = cls.fade_time
        t.fade_delay = cls.fade_delay
        t.fade_in = cls.fade_in        
        t.num_emits = cls.num_emits
        t.num_particles = cls.num_particles
        t.emit_delay = cls.emit_delay
        t.emits_per_sec = cls.emits_per_sec
        t.duration = cls.duration
        cls._tmpl_uptodate = True
            

class PointEmitter(ParticleEmitter):
    _cImpl = _c.ParticleEmitter
    
    angle = 360