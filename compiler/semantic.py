from __future__ import annotations

from .ast_nodes import (
    Assignment, Binary, Block, Identifier, IfStatement, Literal, PrintStatement,
    Program, Unary, VarDeclaration, WhileStatement,
)
from .errors import ErrorReporter
from .symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self) -> None:
        self.symbols = SymbolTable()
        self.reporter = ErrorReporter()

    def analyze(self, program: Program) -> tuple[SymbolTable, ErrorReporter]:
        for statement in program.statements:
            self.visit(statement)
        return self.symbols, self.reporter

    def visit(self, node):
        if isinstance(node, VarDeclaration):
            if not self.symbols.declare(node.name, node.var_type, "global", 0):
                self.reporter.add("SEMANTIC", f"Variable '{node.name}' has already been declared.", 0, 0)
            if node.initializer:
                init_type = self.visit_expr(node.initializer)
                if init_type and not self.assignable(node.var_type, init_type):
                    self.reporter.add("SEMANTIC", f"Cannot assign {init_type} value to {node.var_type} variable '{node.name}'.", 0, 0)
        elif isinstance(node, Assignment):
            symbol = self.symbols.lookup(node.name)
            if symbol is None:
                self.reporter.add("SEMANTIC", f"Variable '{node.name}' is not declared.", 0, 0)
            expr_type = self.visit_expr(node.expression)
            if symbol and expr_type and not self.assignable(symbol.data_type, expr_type):
                self.reporter.add("SEMANTIC", f"Cannot assign {expr_type} value to {symbol.data_type} variable '{node.name}'.", 0, 0)
        elif isinstance(node, PrintStatement):
            self.visit_expr(node.expression)
        elif isinstance(node, IfStatement):
            cond_type = self.visit_expr(node.condition)
            if cond_type and cond_type != "bool":
                self.reporter.add("SEMANTIC", "If condition must be boolean.", 0, 0)
            self.visit(node.then_branch)
            if node.else_branch:
                self.visit(node.else_branch)
        elif isinstance(node, WhileStatement):
            cond_type = self.visit_expr(node.condition)
            if cond_type and cond_type != "bool":
                self.reporter.add("SEMANTIC", "While condition must be boolean.", 0, 0)
            self.visit(node.body)
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.visit(stmt)

    def visit_expr(self, node) -> str | None:
        if isinstance(node, Literal):
            return node.value_type
        if isinstance(node, Identifier):
            symbol = self.symbols.lookup(node.name)
            if symbol is None:
                self.reporter.add("SEMANTIC", f"Variable '{node.name}' is not declared.", 0, 0)
                return None
            return symbol.data_type
        if isinstance(node, Unary):
            operand_type = self.visit_expr(node.operand)
            if node.operator == "!":
                if operand_type and operand_type != "bool":
                    self.reporter.add("SEMANTIC", "Operator '!' requires a boolean operand.", 0, 0)
                    return None
                return "bool"
            if operand_type and operand_type not in {"int", "float"}:
                self.reporter.add("SEMANTIC", f"Unary operator '{node.operator}' requires a numeric operand.", 0, 0)
                return None
            return operand_type
        if isinstance(node, Binary):
            left = self.visit_expr(node.left)
            right = self.visit_expr(node.right)
            if node.operator in {"+", "-", "*", "/", "%"}:
                if left not in {"int", "float", None} or right not in {"int", "float", None}:
                    self.reporter.add("SEMANTIC", f"Operator '{node.operator}' requires numeric operands.", 0, 0)
                    return None
                if left == "float" or right == "float":
                    return "float"
                return "int" if left and right else None
            if node.operator in {">", "<", ">=", "<=", "==", "!="}:
                if left is not None and right is not None and left != right and not ({left, right} <= {"int", "float"}):
                    self.reporter.add("SEMANTIC", f"Incompatible operands for '{node.operator}'.", 0, 0)
                return "bool"
            if node.operator in {"&&", "||"}:
                if left and left != "bool" or right and right != "bool":
                    self.reporter.add("SEMANTIC", f"Operator '{node.operator}' requires boolean operands.", 0, 0)
                    return None
                return "bool"
        return None

    @staticmethod
    def assignable(target: str, source: str) -> bool:
        # Permit widening int -> float.
        return target == source or (target == "float" and source == "int")
