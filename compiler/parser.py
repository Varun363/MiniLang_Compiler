from __future__ import annotations

from .ast_nodes import (
    Assignment, Binary, Block, Identifier, IfStatement, Literal, PrintStatement,
    Program, Unary, VarDeclaration, WhileStatement,
)
from .errors import ErrorReporter
from .tokens import Token, TokenType


class ParseError(Exception):
    pass


class Parser:
    """Recursive-descent parser for the MiniLang grammar."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0
        self.reporter = ErrorReporter()

    def parse(self) -> tuple[Program | None, ErrorReporter]:
        try:
            program = self.program()
            return program, self.reporter
        except ParseError:
            return None, self.reporter

    def program(self) -> Program:
        self.consume(TokenType.PROGRAM, "Expected 'program' at the beginning.")
        name = self.consume(TokenType.IDENTIFIER, "Expected program name after 'program'.")
        self.consume(TokenType.LBRACE, "Expected '{' after program name.")
        statements: list = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            try:
                statements.append(self.statement())
            except ParseError:
                self.synchronize()
        self.consume(TokenType.RBRACE, "Expected '}' at end of program.")
        self.consume(TokenType.EOF, "Unexpected input after program end.")
        return Program(name.lexeme, statements)

    def statement(self):
        if self.match(TokenType.INT, TokenType.FLOAT, TokenType.BOOL):
            return self.declaration(self.previous())
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.check(TokenType.IDENTIFIER):
            return self.assignment()
        self.error(self.peek(), "Expected a declaration, assignment, print, if, or while statement.")
        raise ParseError()

    def declaration(self, type_token: Token) -> VarDeclaration:
        name = self.consume(TokenType.IDENTIFIER, "Expected identifier after data type.")
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after declaration.")
        return VarDeclaration(type_token.lexeme, name.lexeme, initializer)

    def assignment(self) -> Assignment:
        name = self.consume(TokenType.IDENTIFIER, "Expected identifier.")
        self.consume(TokenType.ASSIGN, "Expected '=' in assignment.")
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after assignment.")
        return Assignment(name.lexeme, expr)

    def print_statement(self) -> PrintStatement:
        self.consume(TokenType.LPAREN, "Expected '(' after 'print'.")
        expr = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after print expression.")
        self.consume(TokenType.SEMICOLON, "Expected ';' after print statement.")
        return PrintStatement(expr)

    def if_statement(self) -> IfStatement:
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after if condition.")
        then_branch = self.block()
        else_branch = self.block() if self.match(TokenType.ELSE) else None
        return IfStatement(condition, then_branch, else_branch)

    def while_statement(self) -> WhileStatement:
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after while condition.")
        body = self.block()
        return WhileStatement(condition, body)

    def block(self) -> Block:
        self.consume(TokenType.LBRACE, "Expected '{' to begin block.")
        statements = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            statements.append(self.statement())
        self.consume(TokenType.RBRACE, "Expected '}' after block.")
        return Block(statements)

    def expression(self):
        return self.logical_or()

    def logical_or(self):
        expr = self.logical_and()
        while self.match(TokenType.OR):
            op = self.previous().lexeme
            expr = Binary(expr, op, self.logical_and())
        return expr

    def logical_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            op = self.previous().lexeme
            expr = Binary(expr, op, self.equality())
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQ, TokenType.NEQ):
            op = self.previous().lexeme
            expr = Binary(expr, op, self.comparison())
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GT, TokenType.GTE, TokenType.LT, TokenType.LTE):
            op = self.previous().lexeme
            expr = Binary(expr, op, self.term())
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous().lexeme
            expr = Binary(expr, op, self.factor())
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.previous().lexeme
            expr = Binary(expr, op, self.unary())
        return expr

    def unary(self):
        if self.match(TokenType.NOT, TokenType.MINUS, TokenType.PLUS):
            op = self.previous().lexeme
            return Unary(op, self.unary())
        return self.primary()

    def primary(self):
        if self.match(TokenType.INTEGER):
            return Literal(self.previous().literal, "int")
        if self.match(TokenType.REAL):
            return Literal(self.previous().literal, "float")
        if self.match(TokenType.TRUE):
            return Literal(True, "bool")
        if self.match(TokenType.FALSE):
            return Literal(False, "bool")
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.previous().lexeme)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr
        self.error(self.peek(), "Expected expression.")
        raise ParseError()

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        self.error(self.peek(), message)
        raise ParseError()

    def check(self, token_type: TokenType) -> bool:
        return self.peek().type is token_type

    def advance(self) -> Token:
        if not self.check(TokenType.EOF):
            self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def error(self, token: Token, message: str) -> None:
        self.reporter.add("SYNTAX", message, token.line, token.column)

    def synchronize(self) -> None:
        # Basic error recovery for multiple errors per compilation.
        while not self.check(TokenType.EOF):
            if self.previous().type is TokenType.SEMICOLON:
                return
            if self.peek().type in {
                TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.IF,
                TokenType.WHILE, TokenType.PRINT, TokenType.RBRACE,
            }:
                return
            self.advance()
