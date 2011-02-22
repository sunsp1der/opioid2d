
class RadialVelocityTuple(object):
    def __init__(self, node):
        self._node = node

    def get_direction(self):
        p = self._node._get_physics()
        return p.GetRadialVelocity().x
    def set_direction(self, a):
        p = self._node._get_physics()
        p.SetVelocityAngle(a)
    direction = property(get_direction, set_direction)

    def get_speed(self):
        p = self._node._get_physics()
        return p.GetRadialVelocity().y
    def set_speed(self, s):
        p = self._node._get_physics()
        p.SetVelocitySpeed(s)
    speed = property(get_speed, set_speed)
    
    def __getitem__(self, i):
        if i == 0:
            return self.get_direction()
        elif i == 1:
            return self.get_speed()
        else:
            raise IndexError

    def __setitem__(self, i, value):
        if i == 0:
            self.set_direction(value)
        elif i == 1:
            self.set_speed(value)
        else:
            raise IndexError
