
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

path = [
    (400,300),
    (500,100),
    (650,400),
    (200,500),
    (50,50),
    (500,200),
    ]

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        Display.set_clear_color(None)
        s = TestSprite()
        s.set(
            position = (400,300),
            )
        s.do(
            FollowPath(path, speed=100, curve=200, align=True)
            )

Display.init((800,600), title="FollowPath Test")
Director.run(TestScene)
