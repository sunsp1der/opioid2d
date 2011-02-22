
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "sprites"

class TestScene(Scene):
    layers = ["sprites"]

    def enter(self):
        s1 = TestSprite()
        s1.scale = 4,2
        s1.rect.center = (400,300)

        s2 = TestSprite()
        s2.rect.bottomleft = s1.rect.topleft

        s3 = TestSprite()
        s3.rect.midbottom = s1.rect.midtop

        s4 = TestSprite()
        s4.rect.bottomright = s1.rect.topright

        img = ResourceManager.get_image("sprite.png", hotspot=(1,1))
        s5 = TestSprite(img)
        s5.scale = 3
        s5.rect.midtop = s1.rect.midbottom

Display.init((800,600), title="Opioid2D Sprite Rect Test")
Director.run(TestScene)
