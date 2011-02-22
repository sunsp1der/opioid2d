"""Scene.

"""

__all__ = [
    "Scene",
    "Blend",
    ]

import cOpioid2D as _c
from Opioid2D.internal.objectmgr import ObjectManager
from Opioid2D.public.Director import Director
from Opioid2D.public.Camera import Camera
from Opioid2D.public.Layer import Layer, Blend
from Opioid2D.public.State import State
from Opioid2D.public.gui.GUIManager import GUIManager
from Opioid2D.public.Mouse import Mouse
from Opioid2D.public.Sprite import SpriteGroup

import traceback,sys,pygame
from pygame.locals import *

class Scene(object):
    
    layers = None
    
    def __init__(self):
        self._cObj =_c.Scene()
        self._state = None
        #ObjectManager.register(self)
        layers = self.layers or []
        self.layers = []
        for l in layers:
            self.add_layer(l)
        try:
            _callbacks = SceneCallbacks(self)
            self._cObj.SetCallbacks(_callbacks)
        except:
            traceback.print_exc(sys.stdout)
            raise
        self._callbacks = _callbacks
        self.lights = []

        self._tickfunc = None
        self._realtickfunc = None

        self._init_camera()

        self._set_tick_funcs()
        self._init_collision_detection()
        self._gui = None
        
        self._groups = {}
        
    def get_gui(self):
        if self._gui is None:
            self._gui = GUIManager()
        return self._gui
    gui = property(get_gui)

    def enter(self, *arg, **kw):
        """Callback for entering the scene. Override in a subclass"""
        pass

    def exit(self):
        """Callback for exiting the scene. Override in a subclass"""

    def tick(self):
        """Callback that's called every frame"""

    def realtick(self):
        """Callback that's called every engine tick"""

    def add_layer(self, name):
        self.layers.append(name)
        self._cObj.AddLayer(name)

    def delete_layer(self, name):
        self.layers.remove(name)
        self._cObj.DeleteLayer(name)
        
    def add_group(self, name):
        if name in self._groups:
            raise ValueError("group named %r already exists" % name)
        g = self._cObj.CreateGroup(name)        
        g.thisown = 1
        g = SpriteGroup(g)
        self._groups[name] = g
        return g
    
    def delete_group(self, name):
        pass
    
    def get_group(self, name):
        if name not in self._groups:
            return self.add_group(name)
        return self._groups[name]

    def get_layer(self, name):
        obj = self._cObj.GetLayer(name)
        if obj is None:
            raise ValueError("no such layer: %r" % name)
        return Layer(self, obj)
    
    def get_c_layers(self):
        "Get a list of layer c objects in order from bottom to top"
        return self._cObj.GetLayers()
    
    def set_c_layers(self, layers):
        "Set the list of layer c objects. Generally used for reordering."
        self._cObj.SetLayers(layers)
        mylayers = []
        for layer in layers:
            mylayers.append(layer.GetName())
        self.layers = mylayers
        
    def move_layer(self, layer_name, delta):
        "move_layer(layer_name, delta)-> positive delta moves layer up"
        layers = list(self.get_c_layers())
        idx = 0
        for layer in layers:
            if layer.GetName() == layer_name:
                break
            idx += 1
        if idx != len(layers):
            layers.remove(layer)
            new_idx = max(idx + delta, 0)
            layers.insert( new_idx, layer)
        self.set_c_layers(layers)

    def get_camera(self):
        return self._camera
    def set_camera(self, (x,y)):
        self._camera.position = (x,y)
    camera = property(get_camera, set_camera)

    def set_state(self, _state, *arg, **kw):
        Director.next_state = (_state, arg, kw)
    def get_state(self):
        return self._state
    state = property(get_state, set_state)
    
    def _init_state(self, state):
        if self._state is not None:
            s = self._state
            self._state = None
            s._deinit()
        state, arg, kw = state
        if isinstance(state, type) and issubclass(state, State):
            state = state()
            state.create(*arg, **kw)
        self._state = state
        if state is not None:
            state.enter(*arg, **kw)
        self._set_tick_funcs()
    
    def add_light(self, light):
        self._cObj.AddLight(light._cObj)
        self.lights.append(light)
        
    def remove_light(self, light):
        self._cObj.RemoveLight(light._cObj)
        self.lights.remove(light)

    def set_ambient_light(self, r,g=None,b=None):
        if g is None:
            g = b = r
        c = _c.Color(r,g,b)
        self._cObj.SetAmbientLight(c)

    def _handle_event(self, evname, *args):
        func = None
        funcname = "handle_" + evname
        s = self._state
        if s:
            func = getattr(s, funcname, None)
        if func is None:
            try:
                func = getattr(self, "handle_%s" % evname)
            except AttributeError:
                return
        try:
            func(*args)
        except:
            traceback.print_exc(file=sys.stdout)
            raise
        
    def _handle_events(self, evs):
        h = self._handle_event
        en = pygame.event.event_name
        for ev in evs:
            if hasattr(ev, "pos"):
                x,y = ev.pos
                ev.dict["pos"] = (x*Mouse._mscalex, y*Mouse._mscaley)
            if hasattr(ev, "rel"):
                x,y = ev.rel
                ev.dict["rel"] = (x*Mouse._mscalex, y*Mouse._mscaley)
            h(en(ev.type).lower(), ev)

    def _set_tick_funcs(self):
        s = self._state
        tf = getattr(self, "tick")
        rtf = getattr(self, "realtick")
        if s is not None:
            tf = getattr(s, "tick", None) or tf
            rtf = getattr(s, "realtick", None) or rtf
        if tf != Scene.tick:
            self._tickfunc = tf
        else:
            self._tickfunc = None
        if rtf != Scene.realtick:
            self._realtickfunc = rtf
        else:
            self._realtickfunc = None

    def _init_collision_detection(self):
        self._collision_handlers = {}
        for k in self._get_collision_methods():
            head,group1,group2 = k.split("_")
            self._collision_handlers[group1,group2] = getattr(self, k)
            self._cObj.EnableCollisions(group1, group2)

    def _init_camera(self):
        from Opioid2D.public.Display import Display
        self._camera = Camera(self._cObj.GetCamera())
        w,h = Display.get_view_size()
        self._camera.position = w//2, h//2

    @classmethod
    def _get_collision_methods(cls):
        result = set()
        for b in cls.__bases__:
            if issubclass(b, Scene) and b is not Scene:
                result.update(b._get_collision_methods())
        for k in cls.__dict__:
            if k.startswith("collision_"):
                result.add(k)
                
        return result

    def handle_quit(self, ev):
        Director.quit()
        

class SceneCallbacks(_c.SceneCallbacks):
    def __init__(self, scene):
        _c.SceneCallbacks.__init__(self)
        self.scene = scene

    def OnKeyDown(self, key):
        self.scene._handle_event("keydown", key)

    def OnKeyUp(self, key):
        self.scene._handle_event("keyup", key)

    def OnMouseMotion(self, xrel, yrel):
        self.scene._handle_event("mousemotion", xrel, yrel)

    def OnMouseButtonDown(self, button):
        self.scene._handle_event("mousebuttondown", button)

    def OnMouseButtonUp(self, button):
        self.scene._handle_event("mousebuttonup", button)

    def OnCollision(self, group1, group2, sprite1, sprite2):
        try:
            sprite1 = ObjectManager.c2py(sprite1)
            sprite2 = ObjectManager.c2py(sprite2)
            func = self.scene._collision_handlers[group1,group2]
            func(sprite1, sprite2)
        except:
            traceback.print_exc(file=sys.stdout)
            raise            

    def OnQuit(self):
        self.scene._handle_event("quit")
