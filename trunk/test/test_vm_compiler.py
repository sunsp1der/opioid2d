
from Opioid2D import *

@o2dfunc(IntType, retvalue=IntType)
def addone(a):
    return (
        Return(a + 1),
        )

@o2dfunc(SpriteType, retvalue=VectorType, debugout=True)
def expr(spr):
    return (
        If(spr.position.x < 0).Then(
            spr.position.x <= 0,
            spr.velocity.x <= -spr.velocity.x,
        ),
        
        If(spr.position.y > 600).Then(
            spr.delete()
        ),

        spr.velocity <= spr.velocity * 1.2,

        foo <= 5,
        For(i <= Range(10)).Do(
            spr.position.y <= spr.position.y + (i * 0.1 * foo)
        ),

        bar <= (10,5),
        bar.y <= 10,

        spr.velocity <= (10,5) + bar * 5 - (-spr.acceleration) + (1,2),

        bar, # redundant refernce
        spr.position.x, # redundant property ref
        c <= addone.Call(1),
        addone.Call(2),
        
        Return(bar),
    )
