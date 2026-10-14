"""Run a Lisp source file: python main.py examples/factorial.lisp"""
import argparse
from pathlib import Path
from pyparsing import ParseBaseException
from parser import parse
from runtime import LispError, run


def main():
    cli = argparse.ArgumentParser(description="Minimal Lisp interpreter using pyparsing")
    cli.add_argument("file", type=Path, help="Lisp source file")
    args = cli.parse_args()
    try:
        result = run(parse(args.file.read_text(encoding="utf-8")))
        print(result)
    except (OSError, ParseBaseException, LispError, RecursionError) as exc:
        cli.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
