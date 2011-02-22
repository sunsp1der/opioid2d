"""Node - scenegraph primitive
"""

__all__ = [
    "Node",
    ]

import cOpioid2D as _c
from Opioid2D.public.Director import Director
from Opioid2D.public.actions import Physics
from Opioid2D.public.Layer import Layer
from Opioid2D.internal.objectmgr import ObjectManager
from Opioid2D.internal.radial import RadialVelocityTuple
from Opioid2D.public.Vector import VectorReference, Vector

class NodeBase(object):
    def _on_mgr_delete(self):
        pass

    def do(self, *actions):
        """Perform an action on this Node"""
        for act in actions:
            act.do(self)
        return self

    def set(self, **kw):
        """Set several attributes for this Node"""
        for k,v in kw.iteritems():
            setattr(self, k, v)
        return self

    def attach_to(self, node, back=False):
        """Attach the node to another node
        """
        self._cObj.AttachTo(node._cObj, back)
        return self
    
    def detach(self):
        self._cObj.Detatch()

    def set_position(self, (x, y)):
        self._cObj.SetPos(x,y)
    def get_position(self):
        v = self._cObj.GetPos()
        return VectorReference(v, self)
    position = property(get_position, set_position, doc="Relative position to parent")

    def set_rotation(self, r):
        self._cObj.SetRotation(r)
    def get_rotation(self):
        return self._cObj.GetRotation()
    rotation = property(get_rotation, set_rotation, doc="Angle of rotation in degrees")

    def set_scale(self, scale):
        if isinstance(scale, (tuple, list, Vector)):
            self._cObj.SetScale(_c.Vec2(scale[0], scale[1]))
        else:
            self._cObj.SetScale(scale)
    def get_scale(self):
        v = self._cObj.GetScale()
        return VectorReference(v, self)
    scale = property(get_scale, set_scale, doc="Object scale (xscale,yscale-tuple)")

    ## Physics methods

    def _get_physics(self):
        if self._physics is None:
            self._physics = Physics().do(self)
            self._cObj.physics = self._physics._cObj
        return self._physics._cObj

    def set_velocity(self, (vx, vy)):
        self._get_physics().velocity.set(vx,vy)
    def get_velocity(self):
        v = self._get_physics().velocity
        return VectorReference(v, self)
    velocity = property(get_velocity, set_velocity, doc="Movement velocity (vx,vy-tuple)")

    def set_radial_velocity(self, (angle,speed)):
        self._get_physics().SetRadialVelocity(angle, speed)
    def get_radial_velocity(self):
        return RadialVelocityTuple(self)
    radial_velocity = property(get_radial_velocity, set_radial_velocity, doc="Movement velocity as a (direction,speed)-pair")

    def set_acceleration(self, (ax, ay)):
        self._get_physics().acceleration.set(ax,ay)
    def get_acceleration(self):
        v = self._get_physics().acceleration
        return VectorReference(v, self)
    acceleration = property(get_acceleration, set_acceleration, doc="Acceleration as an (ax,ay)-tuple")

    def set_friction(self, f):
        self._get_physics().friction = f
    def get_friction(self):
        return self._get_physics().friction
    friction = property(get_friction, set_friction, doc="Friction as a multiplier between 0.0-1.0 that is applied at every realtick")

    def set_rotation_speed(self, rot):
        self._get_physics().rotation = rot
    def get_rotation_speed(self):
        return self._get_physics().rotation
    rotation_speed = property(get_rotation_speed, set_rotation_speed)

class Node(NodeBase):
    """
    """
    
    def __init__(self):
        """Initialize a new Node
        
        The newly created Node is not automatically placed in the Scene's
        graph, it has to be placed explicilty using the "place" method.
        """
        self._cObj = _c.Node()
        self._init()

    def _init(self):
        ObjectManager.register(self)
        self.deleted = False
        self._actions = set()
        self._physics = None

    def set_layer(self, layer):
        """Place the node on a layer

        layer - the name of the layer in currently active Scene
        """
        if isinstance(layer, Layer):
            assert layer._scene is Director.GetScene()
            l = layer._layer
        else:
            l = Director.scene._cObj.GetLayer(layer)
        if not l:
            raise ValueError("scene doesn't have a layer called %r" % layer)
        self._cObj.Place(l)
        return self
    def get_layer(self):
        l = self._cObj.GetLayer()
        return l and Layer(Director.GetScene(), l)
    #layer = property(get_layer, set_layer)
    def get_root_layer(self):
        l = self._cObj.GetRootLayer()
        return l and Layer(Director.get_scene(), l)

    def delete(self):
        """Delete the Node from the scenegraph"""
        self.deleted = True
        if self._cObj is not None:
            if not self._cObj.IsDeleted():
                self._cObj.Delete()
        self._end_actions()

    def get_world_position(self):
        v = self._cObj.GetWorldPos()
        return Vector(v.x,v.y)
    world_position = property(get_world_position, doc="Absolute world position")

    def get_world_velocity(self):
        v = self._cObj.GetWorldVelocity()
        return Vector(v.x,v.y)
    world_velocity = property(get_world_velocity, doc="Absolute world velocity")

    def _set_color_inheritance(self, flag):
        self._cObj.SetColorInheritance(flag)
    def _get_color_inheritance(self):
        return self._cObj.GetColorInheritance()
    color_inheritance = property(_get_color_inheritance, _set_color_inheritance)

    def abort_actions(self, type=None):
        if type is None:
            l = self._actions[:]
        else:
            l = [x for x in self._actions if isinstance(x,type)]
        for act in l:
            act.abort()

    def end_actions(self, type=None):
        if type is None:
            l = self._actions[:]
        else:
            l = [x for x in self._actions if isinstance(x,type)]
        for act in l:
            act.end()

    def _end_actions(self):
        for act in self._actions:
            act._node = None
            act.abort()
        self._actions.clear()

    def _on_mgr_delete(self):
        self.delete()
