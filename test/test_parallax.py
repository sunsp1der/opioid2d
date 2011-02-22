
from Opioid2D import *
from random import random

class TestSprite(Sprite):
    image = "sprite.png"

class TestScene(Scene):

    def enter(self):
        for l in range(4):
            layer = "layer %i" % l
            self.add_layer(layer)
            m = l*0.25+0.25
            self.get_layer(layer).set_camera_effect(m)
            node = Sprite()
            node.layer = layer
            node.scale = m
            for x in range(500):
                s = TestSprite()
                s.position = 2000*random()-1000,1000*random()-500
                s.attach_to(node)
        self.camera = 0,0


    def realtick(self):
        key = Keyboard.is_pressed
        cam = self.camera
        if key(K_LEFT):
            cam.velocity.x = -300
        elif key(K_RIGHT):
            cam.velocity.x = 300
        else:
            cam.velocity.x = 0
        if key(K_UP):
            cam.velocity.y = -300
        elif key(K_DOWN):
            cam.velocity.y = 300
        else:
            cam.velocity.y = 0

        if key(K_z):
            cam.scale *= 1.05
        if key(K_x):
            cam.scale *= 0.95

        if key(K_a):
            cam.rotation_speed = -50
        elif key(K_d):
            cam.rotation_speed = 50
        else:
            cam.rotation_speed = 0

Display.init((800,600), title="Opioid Parallax Scroll Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
