
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
        (Delay(1) + CallFunc(self.func, "foo", "bar", foo="bar")).do()

    def func(self, *arg, **kw):
        print arg, kw
        self.sprite.velocity = (200,0)

Display.init((800,600), title="CallFunc Test")
Director.run(TestScene)
