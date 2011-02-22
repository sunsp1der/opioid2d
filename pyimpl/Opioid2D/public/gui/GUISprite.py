
__all__ = [
    "GUISprite",
    ]

from Opioid2D.public.Sprite import Sprite
from Opioid2D.public.Director import Director

class GUISprite(Sprite):
    draggable = False
    
    def __init__(self, img=None):
        self._preinit(img)
        Director.get_scene().gui.register(self)
        self.on_create()

    def unregister(self):
        Director.get_scene().gui.unregister(self)

    def delete(self):
        self.unregister()
        Sprite.delete(self)
        
    def on_enter(self):
        pass
    
    def on_hover(self):
        pass
    
    def on_exit(self):
        pass
    
    def on_press(self):
        pass
    
    def on_release(self):
        pass
    
    def on_click(self):
        pass
        
    def on_rightclick(self):
        pass
    
    def on_drag(self):
        pass
    
    def on_drag_begin(self):
        pass
    
    def on_drag_end(self):
        pass