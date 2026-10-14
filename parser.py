"""Parse a deliberately small Lisp subset into Python nested lists."""
from pyparsing import Forward, Group, OneOrMore, Optional, ParseException, ParserElement, Regex, Suppress, ZeroOrMore


class Symbol(str):
    """Distinguishes Lisp identifiers from future string literals."""


def build_parser():
    expr = Forward()
    # Atom boundaries prevent splitting 123abc into 123 + abc.
    integer = Regex(r"[+-]?\d+(?![^\s()])").set_parse_action(lambda t: int(t[0]))
    symbol = Regex(r"[^\s();]+(?![^\s()])").set_parse_action(lambda t: Symbol(t[0]))
    atom = integer | symbol
    sexpr = Group(Suppress("(") + ZeroOrMore(expr) + Suppress(")"))
    expr <<= (sexpr | atom)
    program = ZeroOrMore(expr)
    program.ignore(Regex(r";[^\n]*"))
    return program


PARSER = build_parser()


def parse(source: str) -> list:
    """Return a sequence of Lisp expressions; reject invalid trailing text."""
    return PARSER.parse_string(source, parse_all=True).as_list()
