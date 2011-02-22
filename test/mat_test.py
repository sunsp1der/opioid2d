
from cOpioid2D import Mat9, Vec2

m = Mat9()
m.identity()
m.rotate(-30)
m.translate(5,10)
m.scale(2,3)

v = Vec2(5,10)

m2 = m.inversed()

print v.x,v.y

m.transform(v)

print v.x,v.y

m2.transform(v)

print v.x,v.y
