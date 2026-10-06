from dataclasses import dataclass


@dataclass
class CompilerError:
    phase: str
    message: str
    line: int
    column: int

    def as_dict(self) -> dict:
        return {
            "phase": self.phase,
            "message": self.message,
            "line": self.line,
            "column": self.column,
        }


class ErrorReporter:
    def __init__(self) -> None:
        self.errors: list[CompilerError] = []

    def add(self, phase: str, message: str, line: int, column: int) -> None:
        self.errors.append(CompilerError(phase, message, line, column))

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    def as_dicts(self) -> list[dict]:
        return [error.as_dict() for error in self.errors]
