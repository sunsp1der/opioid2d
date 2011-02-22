
from Opioid2D import *

class TestSprite(gui.GUISprite):
    image = "button.png"
    layer = "main"

    def on_create(self):
        self.scale = 2

    def on_press(self):
        self.alpha = 0.5

    def on_release(self):
        self.alpha = 1.0

    def on_click(self):
        self.unregister() # stop receiving GUI events
        self.do(ScaleTo(0,secs=0.5) + Delete)

    def on_enter(self):
        self.color = (0.5,1,0.5)

    def on_exit(self):
        self.color = (1,1,1)

class TestScene(Scene):
    layers = [
        "bg",
        "main",
        ]
    
    def enter(self):
        Sprite("opilarge.png").set(layer="bg", position=(400,300))
        for x in range(5):
            s = TestSprite()
            s.position = 100+x*100,300
            s.rotation = x*50

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


Display.init((800,600), title="Opioid2D GUI clicking test")
Director.run(TestScene)
