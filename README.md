# Minimal Lisp on Python and pyparsing

Small Lisp interpreter for SKED `FACTORIAL-GATE`. Parses S-expressions using `pyparsing` and interprets integers, symbols, `define`, `lambda`, `if`, `=`, `-`, `*`, function calls and lexical closures. It supports multiple top-level expressions and `;` comments.

## Debian 13 quick start

```bash
cd mini_lisp_sked
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py examples/factorial.lisp
python -m unittest discover -s tests -v
```

Expected run result: `120`.

## SKED acceptance scope

- `FACTORIAL-GATE` includes factorial for inputs 0, 1, 3, 5 and 10.
- Execution of undefined symbols and malformed syntax fails with an error.
- Not yet a complete Scheme/Common Lisp implementation.
- Negative factorial input is outside the domain. This interpreter has no nonnegative-argument guard, so evaluating negative input will eventually hit Python's recursion limit. Do not treat this as proper domain validation.
- Deep recursion is limited by Python's call stack; tail-call optimization and GC are not implemented separately.
