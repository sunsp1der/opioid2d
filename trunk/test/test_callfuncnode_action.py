
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        self.sprite = s = TestSprite()
        s.set(
            position = (400,300),
            )
        s.do(
            Delay(3) + CallFuncNode(self.func, "foo", "bar", foo="bar")
            )

    def func(self, node, *arg, **kw):
        print node, arg, kw
        node.velocity = (200,0)

Display.init((800,600), title="CallFuncNode Test")
Director.run(TestScene)
