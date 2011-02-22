
from Opioid2D import *

class TestEmitter(PointEmitter):
    image = "particle.png"

    speed = [50,200]
    life = [3,7]
    fade_time = 1    

    num_particles = 5
    num_emits = None
    emit_delay = 0.01

class TestScene(Scene):
    layers = ["particles"]

    def enter(self):
        s = ParticleSystem("particles")
        TestEmitter.emit(s, (400,300))

Display.init((800,600), title="Particle Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
