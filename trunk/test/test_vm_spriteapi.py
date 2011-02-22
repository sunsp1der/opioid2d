
from Opioid2D import *
import unittest

class TestVMSprites(unittest.TestCase):

    def test_sprite_const(self):
        @o2dfunc(retvalue=SpriteType)
        def test():
            return (
                foo <= Sprite(),
                Return(foo),
                )
        ret = test()
        self.assertTrue(isinstance(ret, Sprite))
                
    def test_sprite_scope(self):
        s = Sprite()
        @o2dfunc(retvalue=SpriteType)
        def test():
            return (
                foo <= s,
                Return(foo),
                )
        ret = test()
        self.assertTrue(ret is s)

    def test_get_position(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.position.x <= 10,
                )
        s = Sprite()
        s.position = (0,0)
        test(s)
        self.assertEquals(s.position.x, 10)

    def test_set_position(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.position <= (12,34),
                )
        s = Sprite()
        s.position = (0,0)
        test(s)
        self.assertEquals(s.position.x, 12)
        self.assertEquals(s.position.y, 34)


    def test_get_velocity(self):
        @o2dfunc(SpriteType, retvalue=VectorType)
        def test(spr):
            return (
                Return(spr.velocity),
                )
        s = Sprite()
        s.velocity = 12,34
        ret = test(s)
        self.assertEquals(ret.x, 12)
        self.assertEquals(ret.y, 34)

    def test_set_velocity(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.velocity <= (12,34),
                )
        s = Sprite()
        test(s)
        self.assertEquals(s.velocity.x, 12)
        self.assertEquals(s.velocity.y, 34)

    def test_get_acceleration(self):
        @o2dfunc(SpriteType, retvalue=VectorType)
        def test(spr):
            return (
                Return(spr.acceleration),
                )
        s = Sprite()
        s.acceleration = 12,34
        ret = test(s)
        self.assertEquals(ret.x, 12)
        self.assertEquals(ret.y, 34)

    def test_set_acceleration(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.acceleration <= (12,34),
                )
        s = Sprite()
        test(s)
        self.assertEquals(s.acceleration.x, 12)
        self.assertEquals(s.acceleration.y, 34)


    def test_get_scale(self):
        @o2dfunc(SpriteType, retvalue=VectorType)
        def test(spr):
            return (
                Return(spr.scale),
                )
        s = Sprite()
        s.scale = 12,34
        ret = test(s)
        self.assertEquals(ret.x, 12)
        self.assertEquals(ret.y, 34)

    def test_set_scale(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.scale <= (12,34),
                )
        s = Sprite()
        test(s)
        self.assertEquals(s.scale.x, 12)
        self.assertEquals(s.scale.y, 34)

    def test_get_friction(self):
        @o2dfunc(SpriteType, retvalue=FloatType)
        def test(spr):
            return (
                Return(spr.friction),
                )
        s = Sprite()
        s.friction = 0.5
        ret = test(s)
        self.assertEquals(round(ret,6), 0.5)

    def test_set_friction(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.friction <= 0.5,
                )
        s = Sprite()
        test(s)
        self.assertEquals(round(s.friction,6), 0.5)

    def test_get_rotation(self):
        @o2dfunc(SpriteType, retvalue=FloatType)
        def test(spr):
            return (
                Return(spr.rotation),
                )
        s = Sprite()
        s.rotation = 0.5
        ret = test(s)
        self.assertEquals(round(ret,6), 0.5)

    def test_set_rotation(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.rotation <= 0.5,
                )
        s = Sprite()
        test(s)
        self.assertEquals(round(s.rotation,6), 0.5)

    def test_get_rotation_speed(self):
        @o2dfunc(SpriteType, retvalue=FloatType)
        def test(spr):
            return (
                Return(spr.rotation_speed),
                )
        s = Sprite()
        s.rotation_speed = 0.5
        ret = test(s)
        self.assertEquals(round(ret,6), 0.5)

    def test_set_rotation_speed(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.rotation_speed <= 0.5,
                )
        s = Sprite()
        test(s)
        self.assertEquals(round(s.rotation_speed,6), 0.5)

    def test_get_world_position(self):
        @o2dfunc(SpriteType, retvalue=VectorType)
        def test(spr):
            return (
                Return(spr.world_position),
                )
        s = Sprite()
        s.position = 200,300
        ret = test(s)
        self.assertEqual(round(ret.x, 4), 200)
        self.assertEqual(round(ret.y, 4), 300)
        

    def test_delete(self):
        @o2dfunc(SpriteType)
        def test(spr):
            return (
                spr.delete(),
                )
        s = Sprite()
        test(s)
        self.assertTrue(s._cObj.IsDeleted())
        

if __name__ == '__main__':
    unittest.main()
