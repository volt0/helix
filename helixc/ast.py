from dataclasses import dataclass
from typing import Any, Optional, List


@dataclass
class TypeSignature:
    name: str


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
    body: List[Any]
