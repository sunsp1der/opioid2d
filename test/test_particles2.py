
from Opioid2D import *

class TestEmitter(PointEmitter):
    image = "particle.png"

    direction = 0
    angle = 60

    speed = [0,50]
    acceleration = 5,-30
    friction = 0.99
    
    color = (1, 1, 0, 0.3)
    color_target = (0.5,0,0,0.7)

    scale = [0,2]
    scale_delta = [0,0.5]
    
    life = [3,5]
    fade_time = 2
    fade_in = 2

    num_particles = 5
    emits_per_sec = 100

class TestScene(Scene):
    layers = ["particles"]

    def enter(self):
        s = ParticleSystem("particles")
        TestEmitter.emit(s, (400,500))

Display.init((800,600), title="Particle Test")
fps = Director.run(TestScene)
print "fps %.1f" % fps
