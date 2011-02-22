
from Opioid2D import *

class TestSprite(Sprite):
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        anim = ResourceManager.get_pattern("explosion*.png")        

        s = TestSprite().set(position=(250,300))
        s.do(Animate(anim, secs=1, mode=StopMode))

        s = TestSprite().set(position=(400,300))
        s.do(Animate(anim, secs=1, mode=RepeatMode))

        s = TestSprite().set(position=(550,300))
        s.do(Animate(anim, secs=1, mode=PingPongMode))


Display.init((800,600), title="Animation Test")
Director.run(TestScene)
