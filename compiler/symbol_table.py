from dataclasses import dataclass


@dataclass
class Symbol:
    name: str
    data_type: str
    scope: str
    line: int

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.data_type,
            "scope": self.scope,
            "line": self.line,
        }


class SymbolTable:
    def __init__(self) -> None:
        self.symbols: dict[str, Symbol] = {}

    def declare(self, name: str, data_type: str, scope: str, line: int) -> bool:
        if name in self.symbols:
            return False
        self.symbols[name] = Symbol(name, data_type, scope, line)
        return True

    def lookup(self, name: str) -> Symbol | None:
        return self.symbols.get(name)

    def as_list(self) -> list[dict]:
        return [symbol.as_dict() for symbol in self.symbols.values()]
