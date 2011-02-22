
from Opioid2D import *

class TestScene(Scene):
    def enter(self):
        act = TickFunc(self.foo, "foo")
        act.do()

        act = RealTickFunc(self.foo, "bar")
        act.do()

    def foo(self, x):
        print x

Display.init((800,600), title="TickFunc test")
Director.run(TestScene)
