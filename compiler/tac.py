from __future__ import annotations

from .ast_nodes import (
    Assignment, Binary, Block, Identifier, IfStatement, Literal, PrintStatement,
    Program, Unary, VarDeclaration, WhileStatement,
)


class TACGenerator:
    def __init__(self) -> None:
        self.instructions: list[str] = []
        self.temp_counter = 0
        self.label_counter = 0

    def generate(self, program: Program) -> list[str]:
        self.instructions.clear()
        self.temp_counter = 0
        self.label_counter = 0
        for statement in program.statements:
            self.visit(statement)
        return self.instructions

    def new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self) -> str:
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, text: str) -> None:
        self.instructions.append(text)

    def visit(self, node) -> None:
        if isinstance(node, VarDeclaration):
            if node.initializer:
                value = self.expr(node.initializer)
                self.emit(f"{node.name} = {value}")
        elif isinstance(node, Assignment):
            value = self.expr(node.expression)
            self.emit(f"{node.name} = {value}")
        elif isinstance(node, PrintStatement):
            value = self.expr(node.expression)
            self.emit(f"print {value}")
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, IfStatement):
            cond = self.expr(node.condition)
            else_label = self.new_label()
            end_label = self.new_label()
            self.emit(f"ifFalse {cond} goto {else_label}")
            self.visit(node.then_branch)
            self.emit(f"goto {end_label}")
            self.emit(f"{else_label}:")
            if node.else_branch:
                self.visit(node.else_branch)
            self.emit(f"{end_label}:")
        elif isinstance(node, WhileStatement):
            start_label = self.new_label()
            end_label = self.new_label()
            self.emit(f"{start_label}:")
            cond = self.expr(node.condition)
            self.emit(f"ifFalse {cond} goto {end_label}")
            self.visit(node.body)
            self.emit(f"goto {start_label}")
            self.emit(f"{end_label}:")

    def expr(self, node) -> str:
        if isinstance(node, Literal):
            if node.value_type == "bool":
                return "true" if node.value else "false"
            return str(node.value)
        if isinstance(node, Identifier):
            return node.name
        if isinstance(node, Unary):
            operand = self.expr(node.operand)
            temp = self.new_temp()
            self.emit(f"{temp} = {node.operator}{operand}")
            return temp
        if isinstance(node, Binary):
            left = self.expr(node.left)
            right = self.expr(node.right)
            temp = self.new_temp()
            self.emit(f"{temp} = {left} {node.operator} {right}")
            return temp
        raise TypeError(f"Unsupported AST node: {type(node).__name__}")
