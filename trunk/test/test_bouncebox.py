
from Opioid2D import *
from random import random

class TestEmitter(PointEmitter):
    image = "particle.png"

    speed = [50,200]
    life = [3,7]
    fade_time = 1    

    num_particles = 5
    num_emits = None
    emit_delay = 0.01

class TestScene(Scene):
    layers = [
        "main",
        "particles",
        
        ]
    
    def enter(self):
        for i in range(50):
            s = Sprite("sprite.png")
            s.layer = "main"
            s.join_group("test")
            s.scale = random()*4+0.2
            s.position = (800*random(), 600*random())
            s.velocity = (400*random()-200, 400*random()-200)
        m = mutators.BounceBox(0,0,800,600,userect=True, xmul=0.1, ymul=0.1)
        self.get_group("test").add_mutator(m)
        s = ParticleSystem("particles")
        s.add_mutator(m)
        TestEmitter.emit(s, (400,300))
        
Display.init((800,600), title="Opioid2D BounceBox Test")
Director.run(TestScene)
