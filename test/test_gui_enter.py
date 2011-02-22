
from Opioid2D import *

class TestSprite(gui.GUISprite):
    image = "sprite.png"
    layer = "main"

    def on_create(self):
        self.scale = 2

    def on_enter(self):
        self.color = (0.5,1.0,0.5)

    def on_exit(self):
        self.color = (1,1,1)


class TestScene(Scene):
    layers = [
        "main",
        ]
    
    def enter(self):
        s = TestSprite()
        s.position = 400,300

Display.init((800,600), title="Opioid2D GUI enter/exit test")
Director.run(TestScene)
