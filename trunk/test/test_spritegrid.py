
from Opioid2D import *

class TestSprite(Sprite):
    layer = "main"

class TestScene(Scene):
    layers = [
        "main",
        ]
    
    def enter(self):
        grid = ResourceManager.get_grid("spritegrid.png",16,16)

        s = TestSprite()
        s.position = 200,200
        s.do(Animate(grid[0:2], secs=0.5, mode=RepeatMode))
        
        s = TestSprite()
        s.position = 400,200
        s.do(Animate(grid[2:4], secs=0.5, mode=RepeatMode))

        s = TestSprite()
        s.position = 200,400
        s.do(Animate(grid[4:6], secs=0.5, mode=RepeatMode))

        s = TestSprite()
        s.position = 400,400
        s.do(Animate(grid[6:8], secs=0.5, mode=RepeatMode))

Display.init((800,600), title = "Opioid2D Grid Loading Test")
Director.run(TestScene)
