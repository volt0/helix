from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


@dataclass
class TypeSignature:
    name: str


class VariableMode(Enum):
    let = 0
    var = 1


@dataclass
class VariableSignature:
    name: str
    type: Optional[TypeSignature]
    mode: VariableMode


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
class VariableInitialization(Stmt):
    variable: VariableSignature
    value: Expression


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
