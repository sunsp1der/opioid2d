
from Opioid2D import *

class TestSprite(Sprite):
    image = "sprite.png"
    layer = "main"

class TestScene(Scene):
    layers = [
        "main",
        ]
    
    def handle_mousebuttondown(self, ev):
        s = TestSprite()
        s.position = ev.pos
        
        
Display.init((800,600), (1600,1200), title="Mouse Event Coordinate Test")
Director.run(TestScene)