import unittest
from parser import Symbol, parse
from runtime import LispError, run

DEFINITION = """
(define factorial
  (lambda (n)
    (if (= n 0) 1 (* n (factorial (- n 1))))))
"""


class FactorialTests(unittest.TestCase):
    def test_values(self):
        for value, expected in [(0, 1), (1, 1), (3, 6), (5, 120), (10, 3628800)]:
            with self.subTest(value=value):
                self.assertEqual(run(parse(DEFINITION + f"\n(factorial {value})")), expected)

    def test_parser(self):
        self.assertEqual(parse("(- 12 -3)"), [[Symbol("-"), 12, -3]])
        self.assertEqual(parse("; comment\n(factorial 5)"), [[Symbol("factorial"), 5]])

    def test_undefined_symbol(self):
        with self.assertRaisesRegex(LispError, "Undefined symbol"):
            run(parse("(factorial x)"))

    def test_syntax_error(self):
        with self.assertRaises(Exception):
            parse("(factorial 5")

    def test_non_evaluated_branch(self):
        self.assertEqual(run(parse("(if (= 0 0) 1 unknown)")), 1)

    def test_closure(self):
        self.assertEqual(run(parse("(define make (lambda (x) (lambda (y) (- x y)))) ((make 7) 2)")), 5)


if __name__ == "__main__":
    unittest.main()
