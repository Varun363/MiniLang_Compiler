from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    PROGRAM = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()

    IDENTIFIER = auto()
    INTEGER = auto()
    REAL = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    ASSIGN = auto()
    EQ = auto()
    NEQ = auto()
    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    EOF = auto()


KEYWORDS = {
    "program": TokenType.PROGRAM,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "bool": TokenType.BOOL,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
    literal: Any = None

    def as_dict(self) -> dict:
        return {
            "lexeme": self.lexeme,
            "token": self.type.name,
            "line": self.line,
            "column": self.column,
            "literal": self.literal,
        }
