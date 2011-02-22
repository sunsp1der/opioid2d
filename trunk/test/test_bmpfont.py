
from Opioid2D import *

class TestScene(Scene):
    layers = [
        "text"
        ]
    
    def enter(self):
        Display.SetClearColor((.2,.2,.4))
        font = BitmapFont("testfont.o2f")
        txt = font.create("This is the Opioid2D bitmap font test")
        txt.layer = "text"
        txt.position = 50,200
        for i,l in enumerate(txt.letters):
            if i % 2:
                l.position.y -= 5
                l.do(MoveDelta((0,10), secs=0.5, mode=PingPongMode))
            else:
                l.position.y += 5
                l.do(MoveDelta((0,-10), secs=0.5, mode=PingPongMode))
                
        txt2 = font.create("This is a single sprite", single=True)
        txt2.layer = "text"
        txt2.position = 400,400
        txt2.do(MoveDelta((0,-10), secs=0.5, mode=PingPongMode))
        #txt2.rect.center = 400,400
        
        
Display.init((800,600), title="Opioid2D BitmapFont Test")
Director.run(TestScene)
