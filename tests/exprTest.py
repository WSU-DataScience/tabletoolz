import unittest

from expression import *


class TestUM(unittest.TestCase):


    def test_exp(self):
        e1 = Expr()
        arith_expr = (2 * e1, e1 * 3, e1 - 5, 5 - e1, 2 * e1 - 3)
        assert [f(6) for f in arith_expr] == [12, 18, 1, -1, 9]
        string_expr = (2 * e1, e1 * 3, e1 + "a", "a" + e1)
        assert [f("b") for f in string_expr] == ['bb', 'bbb', 'ba', 'ab']
        bool_expr = (e1 < 3, e1 == 6, e1 <= 2, e1 >= 100, e1 != 6)
        assert tuple(f(6) for f in bool_expr) == (False, True, False, False, False)
        unary_expr = (-e1, +e1, abs(e1))
        assert tuple((f(3), f(-3)) for f in unary_expr) == ((-3, 3), (3, -3), (3, 3))




if __name__ == '__main__':
    unittest.main()

