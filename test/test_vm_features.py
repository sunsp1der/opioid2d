
from Opioid2D import *
import unittest, sys

class TestVM(unittest.TestCase):

    def test_empty(self):
        @o2dfunc()
        def empty():
            return ()
        empty()


    def test_vmcall_params(self):
        @o2dfunc(IntType, retvalue=IntType)
        def foo(a):
            return (
                Return(a+1),
                )
        @o2dfunc(retvalue=IntType)
        def bar():
            return (
                b <= 5,
                Return(foo.Call(b)),
                )
        ret = bar()
        self.assertEquals(ret, 6)

    def test_vmcall(self):
        @o2dfunc(retvalue=IntType)
        def foo():
            return (
                Return(6),
                )
        @o2dfunc(retvalue=IntType)
        def bar():
            return (
                b <= foo.Call(),
                Return(b),
                )
        ret = bar()
        self.assertEquals(ret, 6)

    def test_multi_params(self):
        @o2dfunc(IntType,IntType,FloatType,FloatType, retvalue=VectorType)
        def test(a,b,c,d):
            return (
                v1 <= (a,b),
                v2 <= (c,d),
                Return(v1+v2),
                )
        ret = test(1,2,3,4)
        self.assertEquals(ret.x, 4)
        self.assertEquals(ret.y, 6)

    def test_for(self):
        @o2dfunc(retvalue=IntType)
        def test():
            return (
                s <= 0,
                For(x <= Range(1,6)).Do(
                    s <= s + x,
                ),
                Return(s),
            )
        ret = test()
        self.assertEqual(ret, 15)

    def test_for_return(self):
        @o2dfunc(retvalue=IntType)
        def test():
            return (
                s <= 0,
                For(x <= Range(1,10)).Do(
                    s <= s + x,
                    If(x == 5).Then(
                        Return(s),
                    )
                ),
            )
        ret = test()
        self.assertEqual(ret, 15)
            

    def test_else(self):
        @o2dfunc(retvalue=IntType)
        def test():
            return (
                a <= 5,
                b <= 10,
                If(a > b).Then (
                    c <= 1,
                ).Else(
                    c <= 2,
                ),
                Return(c),
            )
        ret = test()
        self.assertEquals(ret, 2)

    def test_if(self):
        @o2dfunc(retvalue=IntType)
        def test():
            return (
                a <= 5,
                b <= 10,
                If(a < b).Then (
                    c <= 1,
                ).Else(
                    c <= 2,
                ),
                Return(c),
            )
        ret = test()
        self.assertEquals(ret, 1)

    def test_float_const(self):
        @o2dfunc(retvalue=FloatType)
        def test_float():
            return (
                Return(1.2),
                )
        ret = test_float()
        # round because C uses floats and Python uses doubles
        ret = round(ret, 6)
        self.assertEqual(ret, 1.2)

    def test_int_const(self):
        @o2dfunc(retvalue=IntType)
        def test_int():
            return (
                Return(1),
                )
        ret = test_int()
        self.assertEqual(ret, 1)

    def test_vec_const(self):
        @o2dfunc(retvalue=VectorType)
        def test_vec():
            return (
                Return((1,2)),
                )
        ret = test_vec()
        self.assertEqual(ret.x, 1)
        self.assertEqual(ret.y, 2)

    def test_vec_const2(self):
        @o2dfunc(retvalue=VectorType)
        def test_vec2():
            return (
                Return(Vector(1,2)),
                )
        ret = test_vec2()
        self.assertEqual(ret.x, 1)
        self.assertEqual(ret.y, 2)
        
    def test_float_var(self):
        @o2dfunc(retvalue=FloatType)
        def float_var():
            return (
                var <= 1.2,
                Return(var),
                )
        ret = float_var()
        # round because C uses floats and Python uses doubles
        ret = round(ret, 6)
        self.assertEqual(ret, 1.2)
        
    def test_int_var(self):
        @o2dfunc(retvalue=IntType)
        def int_var():
            return (
                var <= 12,
                Return(var),
                )
        ret = int_var()
        self.assertEqual(ret, 12)

    def test_vec_var(self):
        @o2dfunc(retvalue=VectorType)
        def vec_var():
            return (
                var <= (1,2),
                Return(var),
                )
        ret = vec_var()
        self.assertEqual(ret.x, 1)
        self.assertEqual(ret.y, 2)

    def test_getpropv(self):
        @o2dfunc(retvalue=FloatType)
        def prop():
            return (
                var <= (12,34),
                Return(var.x),
                )
        ret = prop()
        ret = round(ret, 4)        
        self.assertEqual(ret, 12)

    def test_setpropv(self):
        @o2dfunc(retvalue=FloatType)
        def prop():
            return (
                var <= (12,34),
                var.x <= 45.6,
                Return(var.x),
                )
        ret = prop()
        ret = round(ret, 4)        
        self.assertEqual(ret, 45.6)

    def test_float_args(self):
        @o2dfunc(FloatType,FloatType,retvalue=FloatType)
        def add(a,b):
            return (
                Return(a + b),
                )
        ret = add(1.2, 3.4)
        ret = round(ret, 6)
        self.assertEqual(ret, 4.6)

    def test_int_args(self):
        @o2dfunc(IntType,IntType,retvalue=IntType)
        def add(a,b):
            return (
                Return(a + b),
                )
        ret = add(12, 34)
        self.assertEqual(ret, 46)
        
    def test_vec_args(self):
        @o2dfunc(VectorType,VectorType,retvalue=FloatType)
        def add(a,b):
            return (
                Return(a.x + b.y),
                )
        ret = add((1,2), Vector(3,4))
        ret = round(ret, 6)
        self.assertEqual(ret, 5)

    def test_add_ff(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3.4,
                Return(a + b),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, 4.6)

    def test_add_fi(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3,
                Return(a + b),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, 4.2)

    def test_add_if(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3,
                Return(b + a),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, 4.2)

    def test_add_ii(self):
        @o2dfunc(retvalue=IntType)
        def add():
            return (
                a <= 12,
                b <= 34,
                Return(a + b),
                )
        ret = add()
        self.assertEqual(ret, 46)

    def test_sub_ff(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3.4,
                Return(a - b),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, -2.2)

    def test_sub_fi(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3,
                Return(a - b),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, -1.8)

    def test_sub_if(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3,
                Return(b - a),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, 1.8)

    def test_sub_ii(self):
        @o2dfunc(retvalue=IntType)
        def add():
            return (
                a <= 12,
                b <= 34,
                Return(a - b),
                )
        ret = add()
        self.assertEqual(ret, -22)

    def test_mul_ff(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3.4,
                Return(a * b),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, 1.2*3.4)

    def test_mul_fi(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3,
                Return(a * b),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, 3.6)

    def test_mul_if(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3,
                Return(b * a),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, 3.6)

    def test_mul_ii(self):
        @o2dfunc(retvalue=IntType)
        def add():
            return (
                a <= 12,
                b <= 34,
                Return(a * b),
                )
        ret = add()
        self.assertEqual(ret, 12*34)

    def test_div_ff(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3.4,
                Return(a / b),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, round(1.2/3.4, 6))

    def test_div_fi(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3,
                Return(a / b),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, round(1.2/3, 6))

    def test_div_if(self):
        @o2dfunc(retvalue=FloatType)
        def add():
            return (
                a <= 1.2,
                b <= 3,
                Return(b / a),
                )
        ret = add()
        ret = round(ret, 6)
        self.assertEqual(ret, round(3/1.2,6))

    def test_div_ii(self):
        @o2dfunc(retvalue=IntType)
        def add():
            return (
                a <= 12,
                b <= 34,
                Return(b / a),
                )
        ret = add()
        self.assertEqual(ret, 34//12)

    def test_add_vv(self):
        @o2dfunc(retvalue=VectorType)
        def add():
            return (
                a <= (12,34),
                b <= (45,56),
                Return(a + b),
                )
        ret = add()
        self.assertEqual(round(ret.x,6), 12+45)
        self.assertEqual(round(ret.y,6), 34+56)

    def test_sub_vv(self):
        @o2dfunc(retvalue=VectorType)
        def add():
            return (
                a <= (12,34),
                b <= (45,56),
                Return(a - b),
                )
        ret = add()
        self.assertEqual(round(ret.x,6), 12-45)
        self.assertEqual(round(ret.y,6), 34-56)

    def test_mul_vf(self):
        @o2dfunc(retvalue=VectorType)
        def add():
            return (
                a <= (12,34),
                b <= 45.6,
                Return(a * b),
                )
        ret = add()
        self.assertEqual(round(ret.x,3), 12*45.6)
        self.assertEqual(round(ret.y,3), 34*45.6)


    def test_bools(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 10,
                c <= (a <= b),
                Return(c),
                )
        ret = test()
        self.assertTrue(ret)

    def test_eqii(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 5,
                Return(a == b)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_eqff(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 5.0,
                Return(a == b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_eqfi(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 5,
                Return(a == b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_eqif(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 5.0,
                Return(a == b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_neii(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6,
                Return(a != b)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_neff(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6.0,
                Return(a != b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_nefi(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6,
                Return(a != b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_neif(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6.0,
                Return(a != b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_ltii(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6,
                Return(a < b)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_ltff(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6.0,
                Return(a < b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_ltfi(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6,
                Return(a < b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_ltif(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6.0,
                Return(a < b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_leii(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6,
                Return(a <= b)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_leff(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6.0,
                Return(a <= b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_lefi(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6,
                Return(a <= b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_leif(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6.0,
                Return(a <= b)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_leii2(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 5,
                Return(a <= b)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_leff2(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 5.0,
                Return(a <= b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_lefi2(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 5,
                Return(a <= b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_leif2(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 5.0,
                Return(a <= b)
                )
        ret = test()
        self.assertTrue(ret)

    def test_geii(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6,
                Return(b >= a)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_geff(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6.0,
                Return(b >= a)
                )
        ret = test()
        self.assertTrue(ret)

    def test_gefi(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6,
                Return(b >= a)
                )
        ret = test()
        self.assertTrue(ret)

    def test_geif(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6.0,
                Return(b >= a)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_geii2(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 5,
                Return(b >= a)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_geff2(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 5.0,
                Return(b >= a)
                )
        ret = test()
        self.assertTrue(ret)

    def test_gefi2(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 5,
                Return(b >= a)
                )
        ret = test()
        self.assertTrue(ret)

    def test_geif2(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 5.0,
                Return(b >= a)
                )
        ret = test()
        self.assertTrue(ret)

    def test_gtii(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6,
                Return(b > a)
                )
        ret = test()
        self.assertTrue(ret)
        
    def test_gtff(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6.0,
                Return(b > a)
                )
        ret = test()
        self.assertTrue(ret)

    def test_gtfi(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5.0,
                b <= 6,
                Return(b > a)
                )
        ret = test()
        self.assertTrue(ret)

    def test_gtif(self):
        @o2dfunc(retvalue=BoolType)
        def test():
            return (
                a <= 5,
                b <= 6.0,
                Return(b > a)
                )
        ret = test()
        self.assertTrue(ret)
        

def tracing(frame, event, arg):
    if event == 'call':
        funcname = frame.f_code.co_name
        if funcname.startswith("test_"):
            print funcname

if __name__ == '__main__':
    #sys.settrace(tracing)
    unittest.main()
