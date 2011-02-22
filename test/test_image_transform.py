
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprite"

class TestScene(Scene):
    layers = ["sprite"]

    def enter(self):
        s = TestSprite()
        s.position = 300,300
        img = s.image

        s2 = Sprite(img.transform("stencil"))
        s2.layer = "sprite"
        s2.position = 500,300

        s3 = Sprite(img.transform("grayscale"))
        s3.layer = "sprite"
        s3.position = 400,400

Display.init((800,600), title="Image Transform Test")
Director.run(TestScene)
