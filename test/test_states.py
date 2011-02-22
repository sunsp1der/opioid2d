
from Opioid2D import *
from random import random

class TestSprite(Sprite):
    image = "sprite.png"

class TestScene(Scene):
    layers = ["main"]

    def enter(self):
        (Delay(1) + SetState(StateA)).do()

    def realtick(self):
        x = random()*800
        y = random()*600
        s = TestSprite()
        s.set(
            position = (x,y),
            layer = "main",
            velocity = (400-x, 300-y),
            )
        s.do(Delay(2) + Delete)

    def handle_keydown(self, ev):
        self.state = StateA
            

class StateA(State):
    def enter(self):
        s = TestSprite()
        s.set(
            layer = "main",
            position = (100,100),
            scale = 4,
            color = (1,1,0)
            )
        s.do(MoveTo((400,200), secs=1) + Delete + SetState(StateB))

    def exit(self):
        s = TestSprite()
        s.set(
            layer = "main",
            position = (200,400),
            scale = 4,
            color = (1,0,0)
            )
        s.do(MoveTo((100,100), secs=1) + Delete)
        

class StateB(State):
    def enter(self):
        (Delay(1) + SetState(StateC)).do()
    
    def realtick(self):
        x = random()*800
        y = random()*600
        s = TestSprite()
        s.set(
            position = (x,y),
            layer = "main",
            velocity = (400-x, 300-y),
            scale = 2,
            )
        s.do(Delay(2) + Delete)
        
class StateC(State):
    layers = [
        "statelayer",
        ]

    def enter(self):
        s = Sprite("opilarge.png")
        s.set(
            position = (400,300),
            alpha = 0.3,
            layer = "statelayer",
            )

    def handle_keydown(self, ev):
        self.scene.state = None


Display.init((800,600), title="Opioid2D State Test")
Director.run(TestScene)
