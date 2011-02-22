
__all__ = [
    "Layer",
    ]

from Opioid2D.internal.objectmgr import ObjectManager

import cOpioid2D as _c

class Blend:
    Zero = 0
    One = 1
    SrcAlpha = 770
    DstAlpha = 772
    MinusSrcAlpha = 771
    MinusDstAlpha = 773
    SrcColor = 768
    MinusSrcColor = 769
    SrcAlphaSaturate = 776

_valid_values = Blend.__dict__.values()

class Layer(object):
    def __init__(self, scene, layer):
        self._scene = scene
        self._layer = layer
        
    def set_camera_effect(self, offset=1.0, zoom=1.0, rotation=1.0):
        self._layer.camera_offset = offset
        self._layer.camera_rotation = rotation
        self._layer.camera_zoom = zoom

    def add_rendering_pass(self, srcfunc, dstfunc):
        if srcfunc not in _valid_values:
            raise ValueError("invalid blend function: %r" % srcfunc)
        if dstfunc not in _valid_values:
            raise ValueError("invalid blend function: %r" % dstfunc)
        rp = _c.RenderingPass()
        rp.thisown = 0
        rp.SetSrcFunc(srcfunc)
        rp.SetDstFunc(dstfunc)
        self._layer.AddRenderingPass(rp)

    def convert_pos(self, x, y):
        v = _c.Vec2(x,y)
        self._scene._camera._cObj.ScreenToWorld(v, self._layer)
        return v.x,v.y

    def pick(self, x, y):
        sprite = self._layer.Pick(_c.Vec2(x,y))
        return ObjectManager.c2py(sprite)
    
    def send_node_to_top(self, node):
        self._cObj.SendNodeToTop( node._cObj)
    
    def send_node_to_bottom(self, node):
        self._cObj.SendNodeToBottom( node._cObj)
        
    def get_node_idx(self, node):
        c_nodes = list(self._layer.GetNodes())
        idx = 0
        the_node = node._cObj
        for c_node in c_nodes:
            # this translates between swig node and swig sprite of same object
            if int(c_node.this) == int(the_node.this):
                break
            idx += 1
        if idx < len(c_nodes):
            return idx
        else:
            return None
        
    def move_node(self, node, delta):
        "move_node(node, delta)-> positive delta moves node up"
        c_nodes = list(self._layer.GetNodes())
        idx = self.get_node_idx( node)
        the_node = c_nodes[idx]
        new_idx = max(0, idx + delta)
        c_nodes.remove( the_node)
        c_nodes.insert( new_idx, the_node)
        self._layer.SetNodes(c_nodes)

    def get_name(self):
        return self._layer.GetName()
    name = property(get_name)
    
    def set_ignore_camera(self, bool):
        self._layer.ignore_camera = bool
    def get_ignore_camera(self):
        return self._layer.ignore_camera
    ignore_camera = property(get_ignore_camera, set_ignore_camera)