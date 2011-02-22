
from Opioid2D import *
from random import random

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "main"
    group = "test"

class TestScene(Scene):
    layers = [
        "main",
        ]
    
    def enter(self):
        m = mutators.BounceBox(0,0,800,600,userect=True)
        self.get_group("test").add_mutator(m)
        for x in range(10):
            s = TestSprite()
            s.position = random()*800, random()*600
        s.radial_velocity = (random()*360, 100)
        s.rotation_speed = 50
            
        self.camera.attach_to(s)
        
    def handle_mousebuttondown(self, ev):
        self.camera.align = not self.camera.align
        
Display.init((800,600), title="Camera Attachment Test")
Director.run(TestScene)