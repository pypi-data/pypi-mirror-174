from dataclasses import dataclass
from functools import partial
from enum import Enum
import operator
import math
from typing import Callable


__all__ = 'Op', 'operators', 'functions',


class OperatorType(str, Enum):
    UNARY = 'unary'
    BINARY = 'binary'


class OperatorDirection(str, Enum):
    RTL = 'rtl'
    LTR = 'ltr'


@dataclass
class Op:
    lit: str
    handler: Callable
    priority: int = 100
    type: OperatorType = OperatorType.BINARY
    dir: OperatorType = OperatorDirection.LTR


Op.Type = OperatorType
Op.Dir = OperatorDirection


operators = [
    Op('-', partial(operator.sub, 0), type=Op.Type.UNARY),
    Op('~', operator.invert, type=Op.Type.UNARY),
    Op('!', operator.not_, type=Op.Type.UNARY),

    Op('**', operator.pow, 400, dir=Op.Dir.RTL),

    Op('*', operator.mul, 200),
    Op('/', operator.truediv, 200),
    Op('//', operator.floordiv, 200),
    Op('%', operator.mod, 200),

    Op('+', operator.add),
    Op('-', operator.sub),
    Op('|', operator.or_),
    Op('&', operator.and_),
    Op('^', operator.xor),

    Op('<=', operator.le, 80),
    Op('>=', operator.ge, 80),
    Op('==', operator.eq, 80),
    Op('<', operator.lt, 80),
    Op('>', operator.gt, 80),
]

functions = {
    # Math
    'abs': operator.abs,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'exp': math.exp,
    'abs': abs,
    'trunc': int,
    'round': round,
    'hypot': math.hypot,

    # Boolean
    'all': lambda *a: all(a),
    'any': lambda *a: any(a),
}