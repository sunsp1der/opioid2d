
from Opioid2D import *
import unittest

class TestVecAPI(unittest.TestCase):

    def test_set_float(self):
        @o2dfunc(retvalue=VectorType)
        def test():
            return (
                v <= (12,34),
                v.set(1.0,2.0),
                Return(v),
                )
        ret = test()
        self.assertEqual(round(ret.x, 6), 1.0)
        self.assertEqual(round(ret.y, 6), 2.0)

    def test_set_int(self):
        @o2dfunc(retvalue=VectorType)
        def test():
            return (
                v <= (12,34),
                v.set(1,2),
                Return(v),
                )
        ret = test()
        self.assertEqual(round(ret.x, 6), 1)
        self.assertEqual(round(ret.y, 6), 2)

    def test_set_intfloat(self):
        @o2dfunc(retvalue=VectorType)
        def test():
            return (
                v <= (12,34),
                v.set(1.0,2),
                Return(v),
                )
        ret = test()
        self.assertEqual(round(ret.x, 6), 1.0)
        self.assertEqual(round(ret.y, 6), 2)

    def test_set_vec(self):
        @o2dfunc(VectorType, retvalue=VectorType)
        def test(src):
            return (
                v <= (12,34),
                v.set(src),
                Return(v),
                )
        a = Vector(56,78)
        ret = test(a)
        self.assertEqual(round(ret.x, 6), 56)
        self.assertEqual(round(ret.y, 6), 78)

    def test_xy(self):
        @o2dfunc(retvalue=VectorType)
        def test():
            return (
                a <= (12,34),
                b <= (56,78),
                a.x <= b.x,
                a.y <= b.y,
                Return(a),
                )
        ret = test()
        self.assertEqual(round(ret.x,4), 56)
        self.assertEqual(round(ret.y,4), 78)

    def test_length(self):
        @o2dfunc(VectorType, retvalue=FloatType)
        def test(v):
            return (
                Return(v.length),
                )
        vec = Vector(12,34)
        ret = test(vec)
        self.assertEqual(round(ret, 4), round(vec.length, 4))

    def test_direction(self):
        @o2dfunc(VectorType, retvalue=FloatType)
        def test(v):
            return (
                Return(v.direction),
                )
        vec = Vector(12,34)
        ret = test(vec)
        self.assertEqual(round(ret, 4), round(vec.direction, 4))


if __name__ == '__main__':
    unittest.main()
