''' opilarge should be centered and scaled to fit the display resolution '''

from Opioid2D import *

class TestSprite(Sprite):
    image = 'opilarge.png' # 800x600
    layer = 'sprite'
    
class TestScene(Scene):
    layers = ['sprite']
    
    def enter(self):
        s = TestSprite()
        s.position = (800,600)
        s.scale = 2
        
Display.init((800,600), units=(1600,1200), title="Viewport test")

Director.run(TestScene)
