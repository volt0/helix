from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TypeSignature:
    name: str


@dataclass
class Expression:
    pass


@dataclass
class IntegerLiteral(Expression):
    value: int


@dataclass
class FloatLiteral(Expression):
    value: float


@dataclass
class BooleanLiteral(Expression):
    value: bool


@dataclass
class Stmt:
    pass


@dataclass
class Return(Stmt):
    expr: Expression


@dataclass
class ReturnVoid(Stmt):
    pass


@dataclass
class Argument:
    name: str
    type: TypeSignature


@dataclass
class Declaration:
    name: str


@dataclass
class FunctionDeclaration(Declaration):
    arguments: List[Argument]
    return_type: Optional[TypeSignature]
    body: List[Stmt]
