
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    group = "test"
    layer = "main"

class TestScene(Scene):
    layers = [
        "main",
        ]
    
    def enter(self):
        for x in range(10):
            s = TestSprite()
            s.set(
                position = (x*50+100,300)
                )
        for sprite in self.get_group("test"):
            sprite.color = 0.5,1.0,0.5

Display.init((800,600), title="Opioid2D SpriteGroup iterator test")
Director.run(TestScene)
