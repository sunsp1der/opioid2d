
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
        self.center = TestSprite().set(position = (400,300))
        self.create_sprite()
        
        
    def create_sprite(self):
        s1 = TestSprite()
        s2 = Sprite("sprite.png")
        s2.position = 10,10
        s2.scale = 0.7
        s2.attach_to(s1)
        s2.do(KeepFacing(self.center))
        s1.position = (800*random(), 600*random())
        s1.radial_velocity = (random()*360, 200)
        s1.do(Delay(2) + Delete)
        (Delay(0.1) + CallFunc(self.create_sprite)).do()
        
Display.init((800,600), title="Attached Delete Test")
Director.run(TestScene)