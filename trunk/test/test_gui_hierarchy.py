
from Opioid2D import *

class TestBG(gui.GUISprite):
    image = "gui_bg.png"
    layer = "main"
    draggable = True


class TestButton(gui.GUISprite):
    image = "button.png"
    draggable = True

    def on_enter(self):
        self.color = 1,1,0.5

    def on_exit(self):
        self.color = 1,1,1

class TestScene(Scene):
    layers = [
        "main",
        ]
    
    def enter(self):
        bg = TestBG()
        bg.position = 400,300

        b1 = TestButton()
        b1.position = -100,100
        b1.attach_to(bg)

        b2 = TestButton()
        b2.position = 100,100
        b2.attach_to(bg)
        

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


Display.init((800,600), title="Opioid2D GUI hierarchy test")
Director.run(TestScene)
