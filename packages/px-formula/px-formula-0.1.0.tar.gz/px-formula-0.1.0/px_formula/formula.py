# Inspired by:
# https://github.com/pyparsing/pyparsing/blob/master/examples/fourFn.py

import operator
from decimal import Decimal
from functools import cached_property, reduce
from itertools import groupby
from typing import Callable, Dict, List, Sequence
from pyparsing import (
    Literal,
    Word,
    Group,
    Forward,
    alphas,
    alphanums,
    Regex,
    CaselessKeyword,
    Suppress,
    delimited_list,
)
from . import defaults
from .defaults import Op
from .exceptions import InvalidIdentifier


__all__ = 'FormulaValue', 'FormulaParsed', 'Formula',


def _group_unsorted(items, key, reverse=False):
    return groupby(sorted(items, key=key, reverse=reverse), key=key)


class FormulaValue(str):
    pass


class FormulaParsed(list):
    pass


class Formula:
    UNARY_PREFIX: str = 'UNARY'

    def __init__(
        self,
        operators: Sequence[Op] = defaults.operators,
        functions: Dict[str, Callable] = defaults.functions,
    ):
        self.operators = operators
        self.functions = functions
        self.__stack__ = FormulaParsed()

    @cached_property
    def unaries(self):
        return {
            x.lit: self.UNARY_PREFIX + x.lit
            for x in self.operators
            if x.type == Op.Type.UNARY
        }

    @cached_property
    def operators_map(self):
        unaries = self.unaries

        return {
            (unaries.get(op.lit, op.lit) if op.type == Op.Type.UNARY else op.lit): op
            for op in self.operators
        }

    @cached_property
    def parser(self):
        functions = reduce(operator.or_, map(CaselessKeyword, self.functions.keys()))
        unary_keys = self.unaries.keys()
        unaries = reduce(operator.or_, map(Literal, unary_keys))
        numbers = Regex(r'[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?')
        variables = Word(alphas, alphanums + '_$')
        lpar, rpar = map(Suppress, '()')

        expr = Forward()
        expr_list = delimited_list(Group(expr))

        # Add parse action that replaces the function identifier with
        # a (name, number of args) tuple:
        fn_call = (functions + lpar - Group(expr_list) + rpar).set_parse_action(
            self._insert_function
        )
        atom = (
            unaries[...]
            +
            (
                (fn_call | variables | numbers).set_parse_action(self._push_first)
                |
                Group(lpar + expr + rpar)
            )
        ).set_parse_action(self._push_unaries)

        factor = Forward()
        binary: List[Op] = [x for x in self.operators if x.type == Op.Type.BINARY]
        # Initializing with something
        factor <<= atom

        for _, items in _group_unsorted(
            binary,
            lambda op: (op.priority, op.dir == op.Dir.RTL),
            reverse=True
        ):
            items = list(items)
            dir = items[0].dir
            collected = reduce(operator.or_, (Literal(x.lit) for x in items))

            # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left
            # exponents, instead of left-to-right that is, 2^3^2 = 2^(3^2), not (2^3)^2.
            if dir == Op.Dir.RTL:
                factor = atom + (collected + factor).set_parse_action(self._push_first)[...]
            else:
                factor = factor + (collected + factor).set_parse_action(self._push_first)[...]

        expr <<= factor

        return expr

    def _insert_function(self, tox):
            fn = tox.pop(0)
            num_args = len(tox[0])
            tox.insert(0, (FormulaValue(fn), num_args))

    def _push_first(self, toks):
        self.__stack__.append(
            FormulaValue(toks[0]) if isinstance(toks[0], str) else toks[0]
        )

    def _push_unaries(self, toks):
        unaries = self.unaries
        for t in toks:
            if t in unaries:
                self.__stack__.append(FormulaValue(unaries[t]))
            else:
                break

    def parse(self, expression: str) -> List[FormulaValue]:
        self.__stack__ = FormulaParsed()
        self.parser.parse_string(expression, parseAll=True)
        result = self.__stack__
        self.__stack__ = FormulaParsed()

        return result

    def as_parsed(self, expression: Sequence[str]) -> List[FormulaValue]:
        return FormulaParsed(
            (
                (FormulaValue(x[0]), x[1])
                if isinstance(x, (list, tuple)) else
                FormulaValue(x)
            )
            for x in expression
        )

    def evaluate(self, stack: List[FormulaValue], variables: dict = {}):
        if not isinstance(stack, FormulaParsed):
            stack = self.as_parsed(stack)

        return self._evaluate(stack, variables=variables)

    def _evaluate(self, stack: List[FormulaValue], variables: dict = {}):
        # TODO: Rework to work non recursively(while cycle)
        op, num_args = stack.pop(), 0
        operators_map = self.operators_map
        functions = self.functions
        raw_op = op

        if isinstance(op, tuple):
            op, num_args, *_ = op + (0, 0,)

        # Values that we didn't parse returned as they are
        if not isinstance(op, FormulaValue):
            return raw_op

        if op in operators_map:
            operator = operators_map[op]

            if operator.type == Op.Type.UNARY:
                return operator.handler(self._evaluate(stack, variables))
            elif operator.type == Op.Type.BINARY:
                # note: operands are pushed onto the stack in reverse order
                op2 = self._evaluate(stack, variables)
                op1 = self._evaluate(stack, variables)

                return operator.handler(op1, op2)

        if op in functions:
            # note: args are pushed onto the stack in reverse order
            args = reversed([self._evaluate(stack, variables) for _ in range(num_args)])
            return functions[op](*args)

        if op in variables:
            return variables[op]

        if op[0].isalpha():
            raise InvalidIdentifier('Invalid identifier "%s".' % op)

        return Decimal(op)

    def __call__(self, formula: str, variables: dict = {}):
        return self.evaluate(self.parse(formula), variables)
