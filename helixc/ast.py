from dataclasses import dataclass
from typing import List, Any


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
    return_type: TypeSignature
    body: Any


@dataclass
class Module:
    declarations: List[Declaration]
