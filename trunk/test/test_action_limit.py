
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.set(
            position = (400,300),
            )
        s.do(
            Move((200,100)).limit(time=1)
            )

Display.init((800,600), title="Action Limit Test")
Director.run(TestScene)
