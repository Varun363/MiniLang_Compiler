from __future__ import annotations

from .lexer import Lexer
from .parser import Parser
from .semantic import SemanticAnalyzer
from .tac import TACGenerator


def ast_to_text(node, prefix="", is_last=True) -> str:
    """Render an AST as an easy-to-read text tree."""
    if node is None:
        return ""
    label = node.__class__.__name__
    if hasattr(node, "name") and node.__class__.__name__ == "Program":
        label += f" ({node.name})"
    elif node.__class__.__name__ == "VarDeclaration":
        label += f" ({node.var_type} {node.name})"
    elif node.__class__.__name__ == "Assignment":
        label += f" ({node.name})"
    elif node.__class__.__name__ == "Binary":
        label += f" ({node.operator})"
    elif node.__class__.__name__ == "Unary":
        label += f" ({node.operator})"
    elif node.__class__.__name__ == "Literal":
        label += f" ({node.value})"
    elif node.__class__.__name__ == "Identifier":
        label += f" ({node.name})"

    lines = [prefix + ("└── " if is_last else "├── ") + label]
    children = []
    if hasattr(node, "statements"):
        children = node.statements
    elif node.__class__.__name__ == "VarDeclaration":
        children = [node.initializer] if node.initializer else []
    elif node.__class__.__name__ == "Assignment":
        children = [node.expression]
    elif node.__class__.__name__ == "PrintStatement":
        children = [node.expression]
    elif node.__class__.__name__ == "IfStatement":
        children = [node.condition, node.then_branch] + ([node.else_branch] if node.else_branch else [])
    elif node.__class__.__name__ == "WhileStatement":
        children = [node.condition, node.body]
    elif node.__class__.__name__ == "Binary":
        children = [node.left, node.right]
    elif node.__class__.__name__ == "Unary":
        children = [node.operand]
    children = [c for c in children if c is not None]
    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(children):
        lines.append(ast_to_text(child, child_prefix, i == len(children) - 1))
    return "\n".join(lines)


def compile_source(source: str) -> dict:
    """Run the source through the educational MiniLang compiler pipeline."""
    result = {
        "success": False,
        "tokens": [],
        "symbol_table": [],
        "ast": None,
        "ast_tree": "",
        "errors": [],
        "tac": [],
        "phases": {
            "lexical": "NOT RUN",
            "syntax": "NOT RUN",
            "semantic": "NOT RUN",
            "intermediate_code": "NOT RUN",
        },
    }

    lexer = Lexer(source)
    tokens, lex_errors = lexer.tokenize()
    result["tokens"] = [t.as_dict() for t in tokens if t.type.name != "EOF"]
    if lex_errors.has_errors:
        result["phases"]["lexical"] = "FAIL"
        result["errors"].extend(lex_errors.as_dicts())
        return result
    result["phases"]["lexical"] = "PASS"

    parser = Parser(tokens)
    program, parse_errors = parser.parse()
    if parse_errors.has_errors or program is None:
        result["phases"]["syntax"] = "FAIL"
        result["errors"].extend(parse_errors.as_dicts())
        return result
    result["phases"]["syntax"] = "PASS"
    result["ast"] = program.to_dict()
    result["ast_tree"] = ast_to_text(program)

    semantic = SemanticAnalyzer()
    symbols, semantic_errors = semantic.analyze(program)
    result["symbol_table"] = symbols.as_list()
    if semantic_errors.has_errors:
        result["phases"]["semantic"] = "FAIL"
        result["errors"].extend(semantic_errors.as_dicts())
        return result
    result["phases"]["semantic"] = "PASS"

    result["tac"] = TACGenerator().generate(program)
    result["phases"]["intermediate_code"] = "PASS"
    result["success"] = True
    return result
