
from Opioid2D import *

cursors = [
    HWCursor.arrow,
    HWCursor.diamond,
    HWCursor.broken_x,
    HWCursor.tri_left,
    HWCursor.tri_right,
    ]

class TestScene(Scene):
    
    def enter(self):
        self.index = 0
        Mouse.cursor = cursors[0]

    def handle_mousebuttondown(self, ev):
        self.index += 1
        self.index %= len(cursors)
        Mouse.cursor = cursors[self.index]

Display.init((800,600), title="Opioid2D Mouse Cursor Test")
Director.run(TestScene)
