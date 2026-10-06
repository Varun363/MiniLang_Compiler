from __future__ import annotations

from .errors import ErrorReporter
from .tokens import KEYWORDS, Token, TokenType


class Lexer:
    """Hand-written lexer for the MiniLang language."""

    TWO_CHAR = {
        ">=": TokenType.GTE,
        "<=": TokenType.LTE,
        "==": TokenType.EQ,
        "!=": TokenType.NEQ,
        "&&": TokenType.AND,
        "||": TokenType.OR,
    }

    ONE_CHAR = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "%": TokenType.PERCENT,
        "=": TokenType.ASSIGN,
        ">": TokenType.GT,
        "<": TokenType.LT,
        "!": TokenType.NOT,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
        ";": TokenType.SEMICOLON,
        ",": TokenType.COMMA,
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.current = 0
        self.start = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1
        self.reporter = ErrorReporter()

    def tokenize(self) -> tuple[list[Token], ErrorReporter]:
        tokens: list[Token] = []
        while not self.is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            token = self.scan_token()
            if token is not None:
                tokens.append(token)
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens, self.reporter

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        ch = self.source[self.current]
        self.current += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def peek(self) -> str:
        return "" if self.is_at_end() else self.source[self.current]

    def peek_next(self) -> str:
        return self.source[self.current + 1] if self.current + 1 < len(self.source) else ""

    def make_token(self, token_type: TokenType, literal=None) -> Token:
        return Token(
            token_type,
            self.source[self.start:self.current],
            self.start_line,
            self.start_column,
            literal,
        )

    def scan_token(self) -> Token | None:
        ch = self.advance()

        if ch in " \r\t":
            return None
        if ch == "\n":
            return None

        # Comments
        if ch == "/" and self.peek() == "/":
            while self.peek() not in ("", "\n"):
                self.advance()
            return None
        if ch == "/" and self.peek() == "*":
            self.advance()
            while not self.is_at_end():
                if self.peek() == "*" and self.peek_next() == "/":
                    self.advance()
                    self.advance()
                    return None
                self.advance()
            self.reporter.add("LEXICAL", "Unterminated block comment.", self.start_line, self.start_column)
            return None

        if ch.isalpha() or ch == "_":
            while self.peek().isalnum() or self.peek() == "_":
                self.advance()
            lexeme = self.source[self.start:self.current]
            token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
            literal = True if token_type is TokenType.TRUE else False if token_type is TokenType.FALSE else None
            return self.make_token(token_type, literal)

        if ch.isdigit():
            while self.peek().isdigit():
                self.advance()
            if self.peek() == "." and self.peek_next().isdigit():
                self.advance()
                while self.peek().isdigit():
                    self.advance()
                return self.make_token(TokenType.REAL, float(self.source[self.start:self.current]))
            return self.make_token(TokenType.INTEGER, int(self.source[self.start:self.current]))

        pair = ch + self.peek()
        if pair in self.TWO_CHAR:
            self.advance()
            return self.make_token(self.TWO_CHAR[pair])

        if ch in self.ONE_CHAR:
            return self.make_token(self.ONE_CHAR[ch])

        self.reporter.add("LEXICAL", f"Invalid character '{ch}'.", self.start_line, self.start_column)
        return None
