
## import everything from Opioid2D 
from Opioid2D import *

## First we define all the sprite classes required in the
## game: ball, paddle and bricks.

class Ball(Sprite):
    image = "gfx/ball.png"
    group = "ball"
    layer = "actors"

    def on_delete(self):
        # If the ball gets deleted, it's game over.
        Director.scene.lose_game()

class Paddle(Sprite):
    image = "gfx/paddle.png"
    group = "paddle"
    layer = "actors"

class Brick(Sprite):
    image = "gfx/brick.png"
    group = "brick"
    layer = "bricks"

    def die(self):
        # Leave the group so that collisions during the fade out
        # perioud will not register.
        self.leave_group("brick")
        self.do(
            AlphaFade(0,secs=0.5) + Delete
            )

    def on_delete(self):
        scene = Director.scene
        # If there are no more bricks left, the player wins.
        if len(scene.get_group("brick")) == 0:
            scene.win_game()


# define the example level layout
LEVEL = [
    " BBBBBBBBB ",
    "BGGYYRYYGGB",
    "BGYRRRRRYGB",
    "BGGYYRYYGGB",
    " BBBBBBBBB ",
    ]

COLORS = {
    'R': (1,0,0),
    'G': (0,1,0),
    'B': (0,1,1),
    'Y': (1,0,1),
    }

class BrickGame(Scene):
    layers = [
        "bg",
        "actors",
        "bricks",
        ]
    
    def enter(self):
        # We fill the whole screen with out background image, so
        # clearing it isn't necessary.
        Display.set_clear_color(None)

        # Load and position the background image.
        bg = Sprite("gfx/bg.png")
        bg.set(
            position = (400,300),
            layer = "bg",
            )
        
        self.generate_bricks(LEVEL)
        
        p = Paddle()
        p.position = 400, 570
        self.paddle = p

        b = Ball()
        b.position = 250,400
        b.radial_velocity = 135,300  # (direction, speed)
        self.ball = b

        # Here we add mutators to the ball's sprite group to control
        # it automatically.
        g = self.get_group("ball")

        # The BounceBox makes the ball bounce off the walls.
        g.add_mutator(
            mutators.BounceBox(23,23,xx=777,yy=700,userect=True)
            )

        # The KillZone deletes the ball if it falls off the screen.
        g.add_mutator(
            mutators.KillZone(0,610,xx=800,yy=700)
            )

        
    def tick(self):        
        p = self.paddle
        k = Keyboard.is_pressed
        if k(K_LEFT):
            p.velocity.x = -450
            p.friction = 1.0
        elif k(K_RIGHT):
            p.velocity.x = 450
            p.friction = 1.0
        else:
            p.friction = 0.92
        if p.rect.left < 30 and p.velocity.x < 0:
            p.velocity.x = 0
        if p.rect.right > 770 and p.velocity.x > 0:
            p.velocity.x = 0

    def generate_bricks(self, layout):
        img = ResourceManager.get_image("gfx/brick.png")
        w,h = img.size
        height = len(layout)*h
        y = 200 - height//2
        for row in layout:
            width = len(row)*w
            x = 400 - width//2 + w//2
            for b in row:
                if b != " ":
                    brick = Brick()
                    brick.set(
                        position = (x,y),
                        color = COLORS[b],
                        )
                x += w
            y += h

    def bounce(self, obstacle):
        b = self.ball
        pos = b.position
        opos = obstacle.position
        rect = obstacle.rect

        # Compare the balls position and velocity to the position
        # of the obstacle to decide which velocity axis we need to
        # invert to bounce it in the right direction.
        if rect.top < pos.y < rect.bottom:
            delta = (b.image.width + obstacle.image.width)/2.0
            if pos.x < opos.x:
                pos.x = opos.x - delta
                b.velocity.x = -abs(b.velocity.x)
            else:
                pos.x = opos.x + delta
                b.velocity.x = abs(b.velocity.x)
        else:
            delta = (b.image.height + obstacle.image.height)/2.0
            if pos.y < opos.y:
                pos.y = opos.y - delta
                b.velocity.y = -abs(b.velocity.y)
            else:
                pos.y = opos.y + delta
                b.velocity.y = abs(b.velocity.y)

    def collision_ball_paddle(self, ball, paddle):
        self.bounce(self.paddle)

        # Transfer some velocity from the paddle to the ball.
        ball.velocity.x += paddle.velocity.x * 0.3

        # Cap the speed of the ball to 300 pixels per second.
        ball.radial_velocity.speed = 300

        # Prevent the ball from bouncing to direct horizontal movement.
        if abs(ball.velocity.y) < 100:
            ball.radial_velocity.direction += 45

    def collision_ball_brick(self, ball, brick):
        self.bounce(brick)
        brick.die()

    def win_game(self):
        (Delay(1) + CallFunc(Director.quit))

    def lose_game(self):
        self.paddle.do(AlphaFade(0, secs=1)+Delete+CallFunc(Director.quit))

Display.init((800,600), title="Opioid Bricks Example")
Director.run(BrickGame)
