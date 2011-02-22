
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        Display.set_clear_color((0,0,0,0.1))
        s = TestSprite()
        s.set(
            position = (100,100),
            velocity = (100, 50),
            )
        

Display.init((800,600), title="Clear Disable Test")
Director.run(TestScene)
