from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class ASTNode:
    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass
class Program(ASTNode):
    name: str
    statements: list[ASTNode]

    def to_dict(self) -> dict[str, Any]:
        return {"type": "Program", "name": self.name, "statements": [s.to_dict() for s in self.statements]}


@dataclass
class Block(ASTNode):
    statements: list[ASTNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"type": "Block", "statements": [s.to_dict() for s in self.statements]}


@dataclass
class VarDeclaration(ASTNode):
    var_type: str
    name: str
    initializer: ASTNode | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"type": "VarDeclaration", "var_type": self.var_type, "name": self.name,
                "initializer": self.initializer.to_dict() if self.initializer else None}


@dataclass
class Assignment(ASTNode):
    name: str
    expression: ASTNode

    def to_dict(self) -> dict[str, Any]:
        return {"type": "Assignment", "name": self.name, "expression": self.expression.to_dict()}


@dataclass
class PrintStatement(ASTNode):
    expression: ASTNode

    def to_dict(self) -> dict[str, Any]:
        return {"type": "PrintStatement", "expression": self.expression.to_dict()}


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: Block
    else_branch: Block | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "IfStatement",
            "condition": self.condition.to_dict(),
            "then_branch": self.then_branch.to_dict(),
            "else_branch": self.else_branch.to_dict() if self.else_branch else None,
        }


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: Block

    def to_dict(self) -> dict[str, Any]:
        return {"type": "WhileStatement", "condition": self.condition.to_dict(), "body": self.body.to_dict()}


@dataclass
class Binary(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

    def to_dict(self) -> dict[str, Any]:
        return {"type": "Binary", "operator": self.operator,
                "left": self.left.to_dict(), "right": self.right.to_dict()}


@dataclass
class Unary(ASTNode):
    operator: str
    operand: ASTNode

    def to_dict(self) -> dict[str, Any]:
        return {"type": "Unary", "operator": self.operator, "operand": self.operand.to_dict()}


@dataclass
class Literal(ASTNode):
    value: Any
    value_type: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "Literal", "value": self.value, "value_type": self.value_type}


@dataclass
class Identifier(ASTNode):
    name: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "Identifier", "name": self.name}
