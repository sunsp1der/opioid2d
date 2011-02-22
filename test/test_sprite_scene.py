
from Opioid2D import *
from Opioid2D.internal.textures import TextureManager

import cOpioid2D as _c
import sys, os, traceback

class TestScene(Scene):
    def enter(self):
        print "TestScene.Enter(self)"
        self.add_layer("test")
        
        for x in range(150):
            for y in range(100):
                s = Sprite("sprite.png")        
                s.position = (x*5, y*5)
                s.rotation = 45;
                s.layer = "test"

    def handle_keydown(self, key):
        Director.quit()

Display.init((800,600), title="Opioid 2D Sprite Scene Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
