
from Opioid2D import *

class TestEmitter(PointEmitter):
    image = "particle.png"

    speed = [50,150]
    life = 3
    fade_time = 2
    fade_in = 1
    color = (1,1,1,0.5)
    offset = [-5,5],[-5,5]

    num_particles = 1000
    num_emits = None
    emits_per_sec = 10

class TestScene(Scene):
    layers = ["particles"]

    def enter(self):
        s = ParticleSystem("particles")
        TestEmitter.emit(s, (400,300))

Display.init((800,600), title="Particle Performance Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
