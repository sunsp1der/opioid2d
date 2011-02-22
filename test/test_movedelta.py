
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.position = (200,200)
        s.do(
            MoveDelta((200,100), secs=1, mode=PingPongMode)
            )

Display.init((800,600), title="MoveDelta Test")
Director.run(TestScene)
