
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s1 = TestSprite()
        s1.set(
            position = (100,50),
            velocity = (50,0),
            )
        parent = Sprite()
        parent.layer = "sprite"
        parent.position = 400,300
        parent.rotation = 0
        parent.rotation_speed = 30
        s2 = Sprite("sprite.png")
        s2.attach_to(parent)
        s2.position = 100,0
        s2.do(KeepFacing(s1, offset=-90))
        

Display.init((800,600), title="Complex KeepFacing Test")
Director.run(TestScene)
