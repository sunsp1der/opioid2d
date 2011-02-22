
from Opioid2D import *
from Opioid2D.internal.textures import TextureManager

import cOpioid2D as _c
import sys, os, traceback

from random import random, choice

class TestScene(Scene):
    layers = [
        "test",
        ]
    
    def enter(self):

        cols = [
            (1,1,1),
            (1,.1,.1),
            (.1,1,.1),
            (.1,.1,1),
            (1,1,.1),
            (1,.1,1),
            (.1,1,1),
            ]

##        for x in range(20):
##            l = Light()
##            l.set_color(*choice(cols))
##            l.set_intensity(15)
##            l.set_cutoff(150)
##            l.set_pos(800*random(),600*random())
##            self.add_light(l)

        self.set_ambient_light(0.3)
        
        for x in range(1000):
            s = Sprite("sprite.png")        
            s.position = (-300+random()*300, random()*400)
            s.velocity = (50+random()*250, random()*100-50)
            s.enable_lighting(True)
            s.acceleration = (0,20)
            s.rotation = 360*random()
            s.layer = "test"
            if x % 100 == 0:
                l = Light()
                l.set_color(10,4,1)
                l.set_intensity(15)
                l.set_cutoff(200)
                l.attach_to(s)
                self.add_light(l)

    def handle_keydown(self, key):
        if key == K_ESCAPE:
            Director.Quit()

Display.init((800,600), title="Opioid 2D Dynamic Lighting Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
