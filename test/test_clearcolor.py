
from Opioid2D import *

class TestScene(Scene):
    def enter(self):
        Display.set_clear_color((1,0,0))

Display.init((800,600), title="ClearColor Test")
Director.run(TestScene)
