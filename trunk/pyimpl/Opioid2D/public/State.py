"""
Different states for Scenes
"""

__all__ = [
    "State",
    ]

from Opioid2D.public.Director import Director

class State(object):
    layers = []
    
    def __init__(self):
        self.scene = Director.GetScene()
        for l in self.layers:
            self.scene.add_layer(l)
        self.create()
        
    def _deinit(self):
        self.exit()
        for l in self.layers:
            self.scene.delete_layer(l)
    
    def create(self, *arg, **kw):
        pass
    
    def enter(self, *arg, **kw):
        pass
    
    def exit(self):
        pass