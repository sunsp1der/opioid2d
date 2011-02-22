from Opioid2D import *

class TestSpriteA(Sprite):
    image = 'sprite.png'
    layer = 'sprite'

class TestSpriteB(Sprite):
    image = 'opilarge.png'
    layer = 'sprite'
    
class TestSceneA(Scene):
    layers = ['sprite']
    
    def enter(self):
        s = TestSpriteA()
        s.position = (400,300)
    
    def handle_keydown(self, evt):
        Director.set_scene(TestSceneB)
        
class TestSceneB(Scene):
    layers = ['sprite']
    
    def enter(self):
        s = TestSpriteB()
        s.position = (400,300)
        s.do(Delay(1.0) + SetScene(TestSceneA))
        
Display.init((800,600), title="Scene change test")
Director.run(TestSceneA)
