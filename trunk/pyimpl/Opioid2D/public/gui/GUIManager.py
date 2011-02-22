
__all__ = [
    "GUIManager",
    ]

import pygame
import pygame.mouse as mouse

from Opioid2D.public.Display import Display
from Opioid2D.public.Director import Director
from Opioid2D.internal.objectmgr import ObjectManager
from Opioid2D.public.Mouse import Mouse
import cOpioid2D as _c

class Drag(object):
    def __init__(self, element, xy):
        self.start_pos = xy
        self.prev_pos = xy
        self._element = element
        
    def _update_pos(self, x, y):
        wx,wy = self._element.get_root_layer().convert_pos(x,y)
        ox,oy = self.prev_pos
        dx = wx-ox
        dy = wy-oy
        self._element.position += (dx,dy)
        self.prev_pos = wx,wy
        

class GUIManager(object):
    def __init__(self):
        self._elements = set()
        self._under = None
        self._drag = None
        self._clicking = None
        
    def register(self, element):
        self._elements.add(element)
        
    def unregister(self, element):
        self._elements.discard(element)
        
    def tick(self, evs):
        mx,my = Mouse.get_position()
        scene = Director.get_scene()
        results = []
        i = 0
        for e in self._elements:
            l = e.get_root_layer()
            wx,wy = l.convert_pos(mx,my)
            p = e._cObj.Pick(_c.Vec2(wx,wy))
            p = ObjectManager.c2py(p)
            if self._drag and self._drag._element is p:
                continue
            if p and p in self._elements:
                idx = scene.layers.index(l.get_name())
                results.append((idx,i,p))
                i += 1
        if not results:
            under = None
        else:
            results.sort()
            under = results[-1][2]
        self._update_under(under)
        if under is not None:
            under.on_hover()
        for ev in evs:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                self._clicking = under
                if under is not None:
                    under.on_press()
            elif ev.type == pygame.MOUSEBUTTONUP:
                if self._drag is not None:
                    self._drag._update_pos(mx,my)
                    self._drag._element.on_drag_end()                    
                    if self._under is not None and self._under is not self._drag._element:
                        self._under.on_exit()
                        self._under = self._drag._element
                    self._drag = None
                    self._clicking.on_release()
                    self._clicking = None
                elif self._clicking is not None:
                    self._clicking.on_release()
                    self._clicking.on_click()
                    self._clicking = None
            elif ev.type == pygame.MOUSEMOTION and self._clicking is under:
                if self._drag is None and under is not None and under.draggable:
                    self._drag = Drag(under,(wx,wy))
                    under.on_drag_begin()
                    self._under = None
        if self._drag is not None:
            self._drag._element.on_drag()
            self._drag._update_pos(mx,my)

    def _update_under(self, under):
        if under is not self._under:
            if self._under is not None:
                self._under.on_exit()
            self._under = under
            if under is not None:
                under.on_enter()
            if self._drag is None and self._clicking is not None:
                self._clicking.on_release()
                self._clicking = None
        
