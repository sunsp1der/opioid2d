
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.position = (200,100)
        s.do(
            MoveDelta((200,0), secs=4, mode=StopMode)
            )

        s = TestSprite()
        s.position = (200,200)
        s.do(
            MoveDelta((200,0), secs=4, mode=PingPongMode)
            )

        s = TestSprite()
        s.position = (200,300)
        s.velocity = 50,0
        s.do(
            Delay(4) + SetAttr(velocity=(0,0))
            )

        

Display.init((800,600), title="MoveDelta Test")
Director.run(TestScene)
