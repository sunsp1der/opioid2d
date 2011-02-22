
from Opioid2D import *

class TestScene(Scene):
    
    def enter(self):
        Mouse.cursor = "particle.png"

    def handle_mousebuttondown(self, ev):
        Mouse.cursor = HWCursor.arrow


Display.init((800,600), title="Opioid2D Mouse Cursor Test")
Director.run(TestScene)
