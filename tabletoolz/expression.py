import operator as op
from toolz import flip, curry


def wrap_magic_method(method_name):
    def wrapped_method(self, *args, **kwargs):
        # TODO: Need to add check for isinstance(other, Expr)
        # TODO: Need to think about dealing with expressions of more than one term.
        return Expr(self.name, func=lambda x: getattr(self(x), "__{}__".format(method_name))(*args, **kwargs))

    return wrapped_method


class Expr(object):
    def __init__(self, name, func=lambda x: x):
        self.expr = func
        self.name = name

    def __call__(self, x):
        return self.expr(x)

    def cast(self, new_type):
        return Expr(self.name, func=lambda x: new_type(self(x)))


for name in ("round", "getitem", "missing", "reversed", "contains"):
    setattr(Expr, "__{}__".format(name), wrap_magic_method(name))


@curry
def get_dunder(name, type_):
    return getattr(type_, name)


def unary_operation(operator):
    return lambda self: Expr(self.name, func=lambda x: operator(self.expr(x)))


def binary_operation(operator):
    return lambda self, other: Expr(self.name, func=lambda x: operator(self.expr(x), other))


def operator_factory(name, right_hand=False, unary=False):
    """ Factory function for constructing magic methods from the operator module"""
    if name in ("and", "or", "not", "is"):
        name += "_"
    o = getattr(op, name)
    if right_hand:
        o = flip(o)
    return unary_operation(o) if unary else binary_operation(o, )


boolean = ("gt", "lt", "ge", "le", "eq", "ne")
arithmetic = ("add", "sub", "mul", "truediv", "floordiv",
              "mod", "pow", "lshift", "rshift", "and", "xor", "or")
unary = ("neg", "pos", "abs", "invert", "not", "index")

for n in boolean:
    setattr(Expr, "__{}__".format(n), wrap_magic_method(n))

for n in arithmetic:
    # Using wrap_magic_method didn't work for __radd__ and strings
    setattr(Expr, "__{}__".format(n), operator_factory(n))
    setattr(Expr, "__r{}__".format(n), operator_factory(n, right_hand=True))

for n in unary:
    setattr(Expr, "__{}__".format(n), wrap_magic_method(n))
