import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from compiler.pipeline import compile_source  # noqa: E402


class MiniLangCompilerTests(unittest.TestCase):
    def test_valid_program(self):
        source = '''program Demo {
            int a;
            int b;
            int result;
            a = 10;
            b = 20;
            result = a + b * 5;
            print(result);
        }'''
        result = compile_source(source)
        self.assertTrue(result["success"])
        self.assertIn("t1 = b * 5", result["tac"])
        self.assertIn("result = t2", result["tac"])

    def test_lexical_error(self):
        result = compile_source("program Demo { int x; x = 10 @ 2; }")
        self.assertFalse(result["success"])
        self.assertEqual(result["phases"]["lexical"], "FAIL")
        self.assertTrue(any(e["phase"] == "LEXICAL" for e in result["errors"]))

    def test_syntax_error(self):
        result = compile_source("program Demo { int x x = 10; }")
        self.assertFalse(result["success"])
        self.assertEqual(result["phases"]["syntax"], "FAIL")

    def test_semantic_error(self):
        result = compile_source("program Demo { y = 10; }")
        self.assertFalse(result["success"])
        self.assertEqual(result["phases"]["semantic"], "FAIL")
        self.assertTrue(any("not declared" in e["message"] for e in result["errors"]))

    def test_control_flow(self):
        source = '''program Demo {
            int x;
            bool ok;
            x = 2;
            ok = x > 0;
            if (ok) { print(x); } else { print(0); }
            while (x > 0) { x = x - 1; }
        }'''
        result = compile_source(source)
        self.assertTrue(result["success"])
        joined = "\n".join(result["tac"])
        self.assertIn("ifFalse", joined)
        self.assertIn("goto", joined)


if __name__ == '__main__':
    unittest.main()
