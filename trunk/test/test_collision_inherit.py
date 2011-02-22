
from Opioid2D import *

class SceneA(Scene):

    def collision_foo_bar(self, foo, bar):
        foo.delete()
        bar.delete()


class SceneB(SceneA):

    layers = [
        "main",
        ]

    def enter(self):
        s1 = Sprite("sprite.png")
        s1.layer = "main"
        s1.join_group("foo")
        s1.position = 200,300
        s1.velocity = 100,0

        s2 = Sprite("sprite.png")
        s2.layer = "main"
        s2.join_group("bar")
        s2.scale = -1,1
        s2.position = 600,300
        s2.velocity = -100,0

Display.init((800,600), title = "O2D collision inheritance test")
Director.run(SceneB)
