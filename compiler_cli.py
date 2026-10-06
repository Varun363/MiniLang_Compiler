from __future__ import annotations

import argparse
from pathlib import Path

from compiler.pipeline import compile_source

DEFAULT = '''program Demo {
    int a;
    int b;
    int result;
    a = 10;
    b = 20;
    result = a + b * 5;
    print(result);
}'''


def main() -> int:
    parser = argparse.ArgumentParser(description="MiniLang command-line compiler")
    parser.add_argument("file", nargs="?", help="Path to a .minilang source file")
    args = parser.parse_args()

    source = Path(args.file).read_text(encoding="utf-8") if args.file else DEFAULT
    result = compile_source(source)

    print("=== PHASE STATUS ===")
    for phase, status in result["phases"].items():
        print(f"{phase:20} {status}")

    print("\n=== TOKENS ===")
    for token in result["tokens"]:
        print(f"{token['line']:>3}:{token['column']:<3} {token['token']:<20} {token['lexeme']}")

    print("\n=== SYMBOL TABLE ===")
    for symbol in result["symbol_table"]:
        print(f"{symbol['name']:<12} {symbol['type']:<8} {symbol['scope']}")

    print("\n=== AST ===")
    print(result["ast_tree"] or "AST not available.")

    print("\n=== ERRORS ===")
    if result["errors"]:
        for error in result["errors"]:
            print(f"[{error['phase']}] line {error['line']}, col {error['column']}: {error['message']}")
    else:
        print("No errors detected.")

    print("\n=== THREE-ADDRESS CODE ===")
    print("\n".join(result["tac"]) if result["tac"] else "Intermediate code not generated.")
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
