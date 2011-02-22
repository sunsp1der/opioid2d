
from Opioid2D import *

class TestEmitter(PointEmitter):
    image = "particle.png"

    speed = [50,150]
    life = 3
    fade_time = 2
    fade_in = 1
    color = (1,1,1,0.5)
    offset = [-5,5],[-5,5]

    num_particles = 50
    num_emits = None
    emits_per_sec = 10

class TestScene(Scene):
    layers = ["particles"]

    def enter(self):
        s = ParticleSystem("particles")
        Emitter1 = TestEmitter.copy()
        Emitter1.color = (1,0,0,0.8)
        Emitter2 = TestEmitter.copy()
        Emitter2.color = (0,1,0,0.8)
        Emitter3 = TestEmitter.copy()
        Emitter3.color = (0,0,1,0.8)
        
        Emitter1.emit(s, (400,200))
        Emitter2.emit(s, (300,350))
        Emitter3.emit(s, (500,350))

Display.init((800,600), title="Emitter Copy Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
