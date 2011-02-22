
from Opioid2D import *
import cOpioid2D as _c
import random

class TestSprite(Sprite):
    image = "opilarge.png"
    layer = "sprite"

class TestImage(Image):
    filename = "large_particle.png"
    mode = "alphamultiplied"

class TestParticle(Sprite):
    image = TestImage
    layer = "particles"

class TestScene(Scene):
    layers = [
        "sprite",
        "particles"
              ]

    def enter(self):
        l = self.get_layer("particles")
        l.add_rendering_pass(
            Blend.Zero,
            Blend.MinusSrcAlpha,
            )
        l.add_rendering_pass(
            Blend.SrcAlpha,
            Blend.One,
            )
        
        random.seed(223)
        s = TestSprite()
        s.set(
            position = (400,300),
            )

        for i in range(5):
            x = 400 + random.random()*100 - 50
            y = 300 + random.random()*100 - 50
            scale = random.random() + 1.5
            s = TestParticle().set(
                position = (x,y),
                scale = scale,
                alpha = 1,
                )
        

Display.init((800,600), title="Additive Blending Test")
Director.run(TestScene)
