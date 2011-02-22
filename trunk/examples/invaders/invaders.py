
from Opioid2D import *
from random import random, choice

class Cannon(Sprite):
    group = "cannon"
    image = "invadersgfx/cannon.png"
    layer = "objects"

    def on_create(self):
        self.shoot_time = 0

    def shoot(self):
        now = Director.get_time()
        if now - self.shoot_time < 60:
            return
        self.shoot_time = now
        for x,angle in [(-3, -10), (0,0), (3, 10)]:
            angle += random()*10-5
            b = Bullet()
            b.position = self.position + (x, -15)
            b.radial_velocity = (angle, 500)
            b.rotation = angle

    def die(self):
        ExplosionParticles.emit(self.system, self.position)
        FlameParticles.emit(self.flames, self.position)
        self.delete()
        act = Delay(2) + CallFunc(Director.quit)
        act.do()        

class Ufo(Sprite):
    group = "ufo"
    image = "invadersgfx/ufo.png"
    layer = "objects"

    shoot_delay = 4

    def on_create(self):
        self.hitpoints = 100
        self.shoot_delay = self.shoot_delay
        self.do(Delay(self.shoot_delay*random()) + CallFunc(self.shoot))
        self.dead = False
        self.targety = random()*300+100

    def damage(self, amount):
        self.hitpoints -= amount
        if self.hitpoints < 0:
            self.die()

    def die(self):
        if self.dead:
            return
        ExplosionParticles.emit(self.system, self.position)
        FlameParticles.emit(self.flames, self.position)
        for i in range(6):
            s = UfoPiece(choice(piecegfx))
            s.set(
                radial_velocity = (random()*200-100, random()*100+50),
                acceleration = (0,180),
                rotation_speed = random()*400-200,
                position = (self.position + (random()*20-10,random()*10-5)),
                )
            act = Delay(random()*0.5+1) + AlphaFade(0, secs=0.4) + Delete
            s.do(act)
            SmokeParticles.emit(self.system, s)
        self.velocity = 0,0
        self.acceleration = 0,0
        self.dead = True
        act = AlphaFade(0, secs=0.5) + Delete
        act.do(self)

    def shoot(self):
        if self.dead:
            return
        bullet = UfoBullet(self.position + (0,10))
        self.do(Delay(self.shoot_delay) + CallFunc(self.shoot))

piecegfx = [
    "invadersgfx/ufopiece1.png",
    "invadersgfx/ufopiece2.png",
    "invadersgfx/ufopiece3.png",
    ]

class UfoPiece(Sprite):
    layer = "objects"

class UfoBulletImage(Image):
    filename = "invadersgfx/ufobullet.png"
    collision = [
        (24,16,12,12),
        ]

class UfoBullet(Sprite):
    group = "ufobullet"
    image = UfoBulletImage
    layer = "explosions"

    def __init__(self, pos):
        Sprite.__init__(self)
        self.set(
            position = pos,
            rotation_speed = 200,
            velocity = (0,200),
            scale = 0.5
            )
        dist = (570-self.position.y)/200.0
        self.do(Delay(dist) + AlphaFade(0,secs=0.3) + Delete)
        UfoBulletParticles.emit(self.system, self)

class BulletImage(Image):
    filename = "invadersgfx/bullet.png"
    hotspot = (0.5, 0.05)
    collision = [
        (0,2,6,6)
        ]

class Bullet(Sprite):
    group = "bullet"
    image = BulletImage
    layer = "objects"

    def die(self):
        BulletParticles.emit(self.system, self.position)
        self.delete()        

class UfoBulletParticles(PointEmitter):
    image = "invadersgfx/particle.png"
    speed = [0,100]
    life = [0.3, 0.6]
    scale = [0.5,1.8]
    color = (0.6,1,0.6,1)

    direction = 0
    angle = 200

    fade_delay = 0
    num_particles = 2
    emit_delay = [0.03,0.2]

class BulletParticles(PointEmitter):
    image = "invadersgfx/particle.png"
    speed = [100,200]
    life = [0.5,1]
    scale = [0.3,1]
    acceleration = [0,100]
    offset = ([-5,5], [-5, 10])
    
    direction = 180
    angle = 160

    fade_delay = 0
    num_particles = [5,10]
    num_emits = 1
    
class SmokeParticles(PointEmitter):
    image = "invadersgfx/smoke.png"
    speed = 0
    scale = 0.3
    scale_delta = 0.3
    life = [1,2]
    fade_delay = 0
    fade_in = 0.2
    color = (.5,.5,.5,.5)
    num_particles = 1
    emits_per_sec = 50
    acceleration = [0,-10]
    duration = [0.8, 1.2]

class ExplosionParticles(PointEmitter):
    image = "invadersgfx/particle.png"
    speed = [30,200]
    life = [0.3,1.5]
    scale = [0.5,1.5]
    acceleration = 0,200    

    color = [1,1,0,1]
    color_target = [1,0,0,1]

    fade_time = 1
    num_particles = 60
    num_emits = 1
    

class FlameImage(Image):
    filename = "invadersgfx/large_particle.png"
    mode = "alphamultiplied"

class FlameParticles(PointEmitter):
    image = FlameImage
    speed = [0,60]
    life = [0.5,0.8]
    scale = [1, 3]
    scale_target = 0.2

    fade_time = 0.4
    fade_in = 0.2
    num_particles = [4,7]
    num_emits = [2,4]
    emit_delay = [0.05, 0.15]

    offset = [-20,20],[-10,10]



class MainScene(Scene):
    layers = [
        "bg",
        "particles",
        "objects",
        "explosions",
        "flame",
        ]
    
    def enter(self):

        ResourceManager.preload_images("invadersgfx/*.png")

        Sprite("invadersgfx/bg.jpg").set(
            position=(400,300),
            layer = "bg",
            )
        
        self.cannon = Cannon()
        self.cannon.position = (400, 580)

        Bullet.system = UfoBullet.system = ParticleSystem("particles")
        Cannon.system = Ufo.system = ParticleSystem("explosions")
        Cannon.flames = Ufo.flames = ParticleSystem("flame")

        l = self.get_layer("flame")
        l.add_rendering_pass(
            Blend.Zero,
            Blend.MinusSrcAlpha,
            )
        l.add_rendering_pass(
            Blend.SrcAlpha,
            Blend.One,
            )

        m = mutators.LifeZone(0,0,800,600)
        self.get_group("bullet").add_mutator(m)

        self.ufo_delay = 5
        self.ufos = set()
        self.create_ufo()

    def create_ufo(self):
        x = random()*500+150
        vx = random()*100+100
        if random() < 0.5:
            vx = -vx
        ufo = Ufo()
        ufo.position = (x,-100)
        ufo.velocity = (vx, 100)
        self.ufos.add(ufo)
        act = Delay(self.ufo_delay) + CallFunc(self.create_ufo)
        if self.ufo_delay > 1:
            self.ufo_delay *= 0.9
        if Ufo.shoot_delay > 1:
            Ufo.shoot_delay *= 0.95
        act.do()

    def realtick(self):
        if not self.cannon.deleted:
            kb = Keyboard
            x,y = self.cannon.position
            if kb.is_pressed(K_LEFT) and x > 100:
                self.cannon.velocity = (-300,0)
            elif kb.is_pressed(K_RIGHT) and x < 700:
                self.cannon.velocity = (300,0)
            else:
                self.cannon.velocity *= 0.8

            if kb.is_pressed(K_SPACE):
                self.cannon.shoot()

        for ufo in self.ufos:
            x,y = ufo.position
            vx,vy = ufo.velocity
            ax,ay = 0,0
            if x < 50 and vx < 100:
                ax = 200
            elif x > 750 and vx > -100:                
                ax = -200
            elif x < 200 and vx < 100:
                ax = 50
            elif x > 600 and vx > -100:                
                ax = -50
            else:
                ax = 0
            if y > ufo.targety and vy > 0:
                ay = -50
            else:
                ay = 0
            ufo.acceleration = ax,ay

    def handle_keydown(self, ev):
        if ev.key == K_ESCAPE:
            Director.quit()

    def collision_bullet_ufo(self, bullet, ufo):
        if ufo.dead:
            return
        bullet.die()
        ufo.damage(20)
        if ufo.dead:
            self.ufos.remove(ufo)

    def collision_cannon_ufo(self, cannon, ufo):
        cannon.die()
        ufo.die()
        self.ufos.remove(ufo)

    def collision_cannon_ufobullet(self, cannon, bullet):
        bullet.delete()
        cannon.die()
        
        
Display.init((800,600), title="Opioid Invaders Demo")
fps = Director.run(MainScene)
print fps
