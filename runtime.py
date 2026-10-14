"""Minimal lexical-environment Lisp evaluator for the factorial example."""
from dataclasses import dataclass
from functools import reduce
from operator import mul
from parser import Symbol


class LispError(Exception):
    pass


class Environment:
    def __init__(self, bindings=None, parent=None):
        self.bindings = dict(bindings or {})
        self.parent = parent

    def get(self, name):
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise LispError(f"Undefined symbol: {name}")

    def define(self, name, value):
        self.bindings[name] = value


@dataclass
class Closure:
    params: list
    body: list
    env: Environment


def expect_integer(value):
    if type(value) is not int:
        raise LispError(f"Expected integer, got {value!r}")
    return value


def subtract(*args):
    if not args:
        raise LispError("'-' expects at least one argument")
    values = [expect_integer(x) for x in args]
    if len(values) == 1:
        return -values[0]
    return values[0] - sum(values[1:])


def multiply(*args):
    return reduce(mul, (expect_integer(x) for x in args), 1)


def equal(*args):
    if len(args) != 2:
        raise LispError("'=' expects exactly two arguments")
    return expect_integer(args[0]) == expect_integer(args[1])


def standard_environment():
    return Environment({"=": equal, "-": subtract, "*": multiply})


def evaluate(expr, env):
    if type(expr) is int or type(expr) is bool:
        return expr
    if isinstance(expr, Symbol):
        return env.get(expr)
    if not isinstance(expr, list) or not expr:
        raise LispError("Expected nonempty expression")

    head = expr[0]
    if head == Symbol("define"):
        if len(expr) != 3 or not isinstance(expr[1], Symbol):
            raise LispError("define syntax: (define name expression)")
        name = expr[1]
        value = evaluate(expr[2], env)
        env.define(name, value)
        return value
    if head == Symbol("lambda"):
        if len(expr) != 3 or not isinstance(expr[1], list) or not all(isinstance(p, Symbol) for p in expr[1]):
            raise LispError("lambda syntax: (lambda (parameters...) expression)")
        if len(set(expr[1])) != len(expr[1]):
            raise LispError("Duplicate lambda parameter")
        return Closure(expr[1], expr[2], env)
    if head == Symbol("if"):
        if len(expr) != 4:
            raise LispError("if syntax: (if condition true-expression false-expression)")
        condition = evaluate(expr[1], env)
        return evaluate(expr[2] if condition is not False else expr[3], env)

    function = evaluate(head, env)
    arguments = [evaluate(arg, env) for arg in expr[1:]]
    if isinstance(function, Closure):
        if len(arguments) != len(function.params):
            raise LispError(f"Expected {len(function.params)} arguments, got {len(arguments)}")
        local = Environment(dict(zip(function.params, arguments)), function.env)
        return evaluate(function.body, local)
    if callable(function):
        try:
            return function(*arguments)
        except TypeError as exc:
            raise LispError(f"Invalid function call: {exc}") from exc
    raise LispError(f"Not a function: {function!r}")


def run(expressions, env=None):
    env = env if env is not None else standard_environment()
    result = None
    for expr in expressions:
        result = evaluate(expr, env)
    return result
