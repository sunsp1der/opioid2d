
from Opioid2D import *
from random import random

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "default"

class TestScene(Scene):
    layers = [
        "bg",
        "default",
        ]

    def enter(self):
        Sprite("opilarge.png").set(
            layer = "bg",
            position = (400,300),
            )
        self.get_layer("bg").ignore_camera = True
        for x in range(1000):
            s = TestSprite()
            s.position = 2000*random(),1000*random()
        self.camera = 1000,500


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

Display.init((800,600), title="Opioid Camera Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
