
__all__ = [
    "StopMode",
    "RepeatMode",
    "PingPongMode",
    
    "Action",

    "Delete",
    "SetAttr",
    "SetNode",

    "Fork",
    "Repeat",

    "Delay",
    "CallFunc",
    "CallFuncNode",
    "TickFunc",
    "RealTickFunc",
    
    "SetScene",
    "SetState",

    "Move",
    "MoveDelta",
    "MoveTo",
    "FollowPath",

    "RotateDelta",
    "Rotate",
    "RotateTo",
    "KeepFacing", # TODO: needs a better name
    "OrbitAround",
    
    "Scale",
    "ScaleTo",

    "AlphaFade",
    "ColorFade",
    
    "Animate",
    ]

import sys, traceback

import cOpioid2D as _c
from copy import copy
from Opioid2D.internal.objectmgr import ObjectManager
from Opioid2D.public.Vector import Vector, VectorReference
from Opioid2D.public.Director import Director
from Opioid2D.public.Math import angledelta
from Opioid2D.public.ResourceManager import ResourceManager

class Action(object):

    def __init__(self):
        self._next = None
        self._node = None
        self._limit = None
        self._aborted = False

    aborted = property(lambda self: self._aborted)

    def __add__(self, other):
        obj = self.copy()
        obj.chain(other)
        return obj

    def __iadd__(self, other):
        self.chain(other)
        return self

    def copy(self):
        obj = copy(self)
        if self._next is not None:
            obj._next = self._next.copy()
        return obj
    
    def chain(self, other):
        if self._next is not None:
            self._next.chain(other)
        else:
            if type(other) is type:
                other = other()
            else:
                other = other.copy()
            self._next = other

    def limit(self, time):
        if time < 0:
            time = 0
        self._limit = time
        return self

    def end(self):
        if hasattr(self, "_cObj") and self._cObj is not None:
            self._cObj.End()
        else:
            self.on_end()

    def abort(self):
        self._aborted = True
        self.end()

    def __radd__(self, other):
        if type(other) is type:
            other = other()
        else:
            other = other.copy()
        other.chain(self)
        

    def do(self, *actors):
        if not actors:
            actors = [None]
        result = []
        for node in actors:
            obj = self.copy()
            obj._callbacks = None
            obj._node = node
            obj.activate()
            result.append(obj)
        if len(result) == 1:
            return result[0]
        return result

    def activate(self):
        if self._node is not None:
            if self._node.deleted:
                self._aborted = True
                return
            self._node._actions.add(self)
        self.on_activate()

    def on_activate(self):
        pass

    def on_end(self):
        if self._node is not None:
            self._node._actions.discard(self)
        if self.aborted:
            return
        try:
            if self._next is not None:
                self._next._node = self._node
                self._next.activate()
        except:
            traceback.print_exc(sys.stdout)
            sys.stdout.flush()
            raise

    def on_wake(self):
        pass

    def _on_mgr_delete(self):
        #print "action del"
        #self._callbacks = None
        pass

#    def __del__(self):
#        self._callbacks = None
#        self._node = None
#        self._next = None

class ActionCallbackImpl(_c.ActionCallbacks):
    def __init__(self, action):
        _c.ActionCallbacks.__init__(self)
        self.action = action
    
    def End(self):
        try:
            self.action.on_end()
            self.action._callbacks = None
            self.action = None
        except:
            traceback.print_exc(file=sys.stdout)
            raise

    def Wake(self):
        try:
            self.action.on_wake()
        except:
            traceback.print_exc(file=sys.stdout)
            raise

## Pure Python actions

class Delete(Action):
    def on_activate(self):
        n = self._node
        self._node = None
        self.on_end()
        if n is not None:
            n.delete()

class SetAttr(Action):
    def __init__(self, **kw):
        self.kw = kw
        Action.__init__(self)
    
    def on_activate(self):
        if self._node is not None:
            self._node.set(**self.kw)
        self.on_end()

class Fork(Action):
    def __init__(self, *actions):
        self.actions = actions
        Action.__init__(self)

    def on_activate(self):
        for act in self.actions:
            act.do(self._node)
        self.on_end()

class Repeat(Action):
    def __init__(self, action, repeats=None):
        self.action = action
        self.repeats = repeats
        Action.__init__(self)

    def on_activate(self):
        if self.repeats is None:
            do = True
        elif self.repeats > 0:
            do = True
            self.repeats -= 1
        else:
            do = False
        if do:
            act = self.action.copy() + CallFunc(self.activate)
            act.do(self._node)
        else:
            self.on_end()

class CallFunc(Action):
    def __init__(self, _func, *arg, **kw):
        self.func = _func
        self.arg = arg
        self.kw = kw
        Action.__init__(self)

    def on_activate(self):
        self.func(*self.arg, **self.kw)
        self.on_end()

class CallFuncNode(CallFunc):
    def on_activate(self):
        self.func(self._node, *self.arg, **self.kw)

class SetNode(Action):
    def __init__(self, node):
        self.new_node = node
        Action.__init__(self)

    def activate(self):
        self._node = self.new_node
        if self._node is not None and self._node.deleted:
            self._aborted = True
            return
        self.on_end()

class SetScene(Action):
    def __init__(self, scene, *arg, **kw):
        Action.__init__(self)
        self.scene = scene
        self.arg = arg
        self.kw = kw

    def on_activate(self):
        Director.set_scene(self.scene, *self.arg, **self.kw)
        self.on_end()

class SetState(Action):
    def __init__(self, state):
        Action.__init__(self)
        self.state = state

    def on_activate(self):
        Director.scene.state = self.state
        self.on_end()

## C++ Actions

StopMode = 0
RepeatMode = 1
PingPongMode = 2

class _CAction(Action):
    _needs_node = True
    _needs_sprite = False
    
    def _Cactivate(self, cls, *arg):
        self._Cprepare(cls, *arg)
        ObjectManager.register(self)
        self._cObj.Start()

    def _Cprepare(self, cls, *arg):
        self._callbacks = ActionCallbackImpl(self)
        self._cObj = cls(*arg)
        if self._node is None:
            if self._needs_node:
                raise ValueError("%s action needs a target Node" % self.__class__.__name__)
            target = None
        else:
            target = self._node._cObj
            if self._needs_sprite and not isinstance(target, _c.Sprite):
                raise TypeError("%s action needs a Sprite as the target Node" % self.__class__.__name__)
        #self._cObj.target = target
        #self._cObj.callbacks = self._callbacks
        self._cObj.Setup(target, self._callbacks)
        if self._limit is not None:
            self._cObj.SetTimeLimit(self._limit)
        
class Physics(_CAction):
    
    def on_activate(self):
        self._Cactivate(_c.Physics);

class Move(_CAction):
    def __init__(self, velocity):
        Action.__init__(self)
        self.velocity = velocity
    
    def on_activate(self):
        self._Cactivate(_c.Move, _c.Vec2(*self.velocity))

class Delay(_CAction):
    _needs_node = False
    
    def __init__(self, secs):
        Action.__init__(self)
        self.secs = secs

    def on_activate(self):
        self._Cactivate(_c.Delay, self.secs)

class IntervalAction(_CAction):
    def __init__(self, secs, mode=StopMode):
        Action.__init__(self)
        self.secs = secs
        self.mode = mode
        self.fadein = None
        
    def smooth(self, fadein, fadeout):
        self.fadein = fadein
        self.fadeout = fadeout
        return self

    def _Cactivate(self, cls, *arg):
        self._Cprepare(cls, *arg)
        if self.mode not in (StopMode, RepeatMode, PingPongMode):
            raise ValueError("invalid mode for interval action: %r" % self.mode)
        self._cObj.SetInterval(self.secs, self.mode)
        if self.fadein is not None:
            self._cObj.SetSmoothing(self.fadein, self.fadeout)
        self._cObj.Start()
        ObjectManager.register(self)

class MoveDelta(IntervalAction):
    def __init__(self, delta, secs, mode=StopMode):
        IntervalAction.__init__(self, secs, mode)
        self.delta = delta

    def on_activate(self):
        self._Cactivate(_c.MoveDelta, _c.Vec2(*self.delta))

class MoveTo(MoveDelta):
    def __init__(self, pos, secs, mode=StopMode):
        IntervalAction.__init__(self, secs, mode)
        self.pos = pos

    def on_activate(self):
        self._Cactivate(_c.MoveTo, _c.Vec2(*self.pos))

class AlphaFade(IntervalAction):
    def __init__(self, dstalpha, secs, mode=StopMode):
        IntervalAction.__init__(self, secs, mode)
        self.dstalpha = dstalpha

    def on_activate(self):
        self._Cactivate(_c.AlphaFade, self.dstalpha)

class ColorFade(IntervalAction):
    def __init__(self, dstcolor, secs, mode=StopMode):
        IntervalAction.__init__(self, secs, mode)
        self.color = dstcolor        

    def on_activate(self):
        self._Cactivate(_c.ColorFade, _c.Color(*self.color))

class RotateDelta(IntervalAction):
    def __init__(self, delta, secs, mode=StopMode):
        IntervalAction.__init__(self, secs, mode)
        self.delta = delta

    def on_activate(self):
        self._Cactivate(_c.RotateDelta, self.delta)

class RotateTo(IntervalAction):
    def __init__(self, target, secs=None, speed=None, dir=0, mode=StopMode):
        IntervalAction.__init__(self, secs, mode)
        self.target = target
        self.speed = speed
        self.dir = dir

    def on_activate(self):
        if self.dir == 0:
            delta = angledelta(self._node.rotation, self.target)
        else:
            delta = self._node.rotation - self.target
            if delta < 0 and self.dir == 1:
                delta += 360
            elif delta > 0 and self.dir == -1:
                delta -= 360
        if self.speed is not None:
            self.secs = abs(delta/self.speed)
        self._Cactivate(_c.RotateDelta, delta)


class KeepFacing(_CAction):
    def __init__(self, target, offset=0):
        Action.__init__(self)
        self.target = target
        self.offset = offset
        
    def on_activate(self):
        self._Cactivate(_c.KeepFacing, self.target._cObj, self.offset)

class OrbitAround(_CAction):
    def __init__(self, target, speed, align=False):
        Action.__init__(self)
        self.target = target
        self.speed = speed
        self.align = align
        
    def on_activate(self):
        self._Cactivate(_c.OrbitAround, self.target._cObj, self.speed, self.align)

class Rotate(_CAction):
    def __init__(self, speed):
        Action.__init__(self)
        self.speed = speed        

    def on_activate(self):
        self._Cactivate(_c.Rotate, self.speed)

class Scale(_CAction):
    def __init__(self, speed, multiply=True):
        Action.__init__(self)
        self.speed = speed
        self.multiply = multiply

    def on_activate(self):
        self._Cactivate(_c.Scale, self.speed, self.multiply)

class ScaleTo(IntervalAction):
    def __init__(self, dstscale, secs, mode=StopMode):
        IntervalAction.__init__(self, secs, mode)
        if isinstance(dstscale, (tuple, list, Vector)):
            self.dstscale = dstscale
        else:
            self.dstscale = (dstscale, dstscale)

    def on_activate(self):
        self._Cactivate(_c.ScaleTo, _c.Vec2(*self.dstscale))

class TickFunc(_CAction):
    _needs_node = False
    
    def __init__(self, func, *arg, **kw):
        Action.__init__(self)
        self._func = func
        self._arg = arg
        self._kw = kw

    def on_activate(self):
        self._Cactivate(_c.TickFunc, False)

    def on_wake(self):
        self._func(*self._arg, **self._kw)

class RealTickFunc(TickFunc):
    def on_activate(self):
        self._Cactivate(_c.TickFunc, True)


class FollowPath(_CAction):

    def __init__(self, points, curve, speed, align=True):
        Action.__init__(self)
        self.points = points
        self.lead = curve
        self.speed = speed
        self.align = align

    def on_activate(self):
        self._Cprepare(_c.FollowPath, len(self.points), self.lead, self.align)
        ObjectManager.register(self)
        for i,p in enumerate(self.points):
            self._cObj.SetPoint(i, _c.Vec2(*p))
        self._cObj.SetSpeed(self.speed)
        self._cObj.Start()
        
    def set_speed(self, speed):
        self._cObj.SetSpeed(speed)
        
        
        
class Animate(_CAction):
    _needs_sprite = True
    
    def __init__(self, frames, fps=None, secs=1, mode=StopMode, start_frame=0, start_direction=1):
        _CAction.__init__(self)
        if isinstance(frames, basestring):
            frames = ResourceManager.get_pattern(frames)
        self.frames = frames
        if fps is not None:
            self.delay = 1.0/fps
        else:
            self.delay = float(secs)/len(self.frames)
        self.mode = mode
        self.frame = start_frame
        self.direction = start_direction

    def on_activate(self):
        if not self.frames:
            raise ValueError("no animation frames given")
        if len(self.frames) == 1:
            self._node.set_image(self.frames[0])
            return
        self._Cactivate(_c.Animate, self.delay)
        self._node.set_image(self.frames[self.frame])

    def on_wake(self):
        self.frame += self.direction
        if self.frame >= len(self.frames):
            if self.mode == StopMode:
                self.end()
                return
            elif self.mode == RepeatMode:
                self.frame = 0
            elif self.mode == PingPongMode:
                self.direction = -1
                self.frame = len(self.frames)-2
        if self.frame < 0:
            self.frame = 1
            self.direction = 1
        self._node.set_image(self.frames[self.frame])
