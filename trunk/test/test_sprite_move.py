
from Opioid2D import *
from Opioid2D.internal.textures import TextureManager

import cOpioid2D as _c
import sys, os, traceback

from random import random

class TestScene(Scene):
    layers = [
        "test",
        ]
    
    def enter(self):
        print "TestScene.Enter(self)"
        self.add_layer("test")
        
        for x in range(15000):
            s = Sprite("sprite.png")
            s.position = (-300+random()*300, random()*400)
            s.velocity = (150+random()*150, 0)
            s.acceleration = (0,80*random())
            s.layer = "test"

    def handle_keydown(self, key):
        Director.quit()

Display.init((800,600), title="Opioid 2D Sprite Move Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
