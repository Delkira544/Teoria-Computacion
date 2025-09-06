from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, unique
import re
from typing import Iterator, Dict, Callable, Pattern

@unique
class Category(Enum):
    KEYWORD = "KEYWORD"
    IDENT = "IDENT"
    LIT_INT = "LIT_INT"
    LIT_FLOAT = "LIT_FLOAT"
    LIT_STRING = "LIT_STRING"
    OPERATOR = "OPERATOR"
    PUNCT = "PUNCT"
    EOF = "EOF"
    ERROR = "ERROR"

@dataclass(frozen=True)
class Token:
    category: Category
    kind: str
    lexeme: str
    line: int
    col: int
    value: int | float | str | None = None

    def __str__(self) -> str:
        base = f"{self.category.value}:{self.kind} '{self.lexeme}' ({self.line}:{self.col})"
        if self.value is not None:
            base += f" value={self.value}"
        return base

class TokenRegistry:
    def __init__(self):
        # Keywords básicas de Python
        self.keywords: Dict[str, str] = {
            "and": "AND", "or": "OR", "not": "NOT",
            "if": "IF", "elif": "ELIF", "else": "ELSE",
            "while": "WHILE", "for": "FOR", "in": "IN",
            "def": "DEF", "return": "RETURN", "pass": "PASS",
            "class": "CLASS", "import": "IMPORT", "from": "FROM", "as": "AS",
            "try": "TRY", "except": "EXCEPT", "finally": "FINALLY",
            "with": "WITH", "lambda": "LAMBDA",
            "True": "TRUE", "False": "FALSE", "None": "NONE",
            "break": "BREAK", "continue": "CONTINUE",
            "is": "IS", "del": "DEL", "global": "GLOBAL", "nonlocal": "NONLOCAL",
        }
        
        # Operadores de Python
        self.operators: Dict[str, str] = {
            # Aritméticos
            "+": "PLUS", "-": "MINUS", "*": "STAR", "/": "SLASH", 
            "//": "DOUBLESLASH", "%": "PERCENT", "**": "DOUBLESTAR",
            # Asignación
            "=": "ASSIGN", "+=": "PLUSEQUAL", "-=": "MINUSEQUAL", 
            "*=": "STAREQUAL", "/=": "SLASHEQUAL", "//=": "DOUBLESLASHEQUAL",
            "%=": "PERCENTEQUAL", "**=": "DOUBLESTAREQUAL",
            # Comparación
            "==": "EQEQUAL", "!=": "NOTEQUAL", "<": "LESS", ">": "GREATER",
            "<=": "LESSEQUAL", ">=": "GREATEREQUAL",
        }
        
        # Puntuación de Python
        self.punctuation: Dict[str, str] = {
            "(": "LPAR", ")": "RPAR", "[": "LSQB", "]": "RSQB",
            "{": "LBRACE", "}": "RBRACE", ",": "COMMA", ":": "COLON",
            ";": "SEMI", ".": "DOT",
        }

    def _create_alternation(self, symbols: list[str]) -> str:
        if not symbols:
            return r"(?!x)x"
        # Ordenar por longitud descendente para evitar problemas con operadores como ** vs *
        return "|".join(re.escape(s) for s in sorted(symbols, key=len, reverse=True))

    def build_regex_pattern(self) -> str:
        kw_alt = self._create_alternation(list(self.keywords.keys()))
        op_alt = self._create_alternation(list(self.operators.keys()))
        punct_alt = self._create_alternation(list(self.punctuation.keys()))

        return rf"""
            (?P<WS>        [ \t]+ )         1                            |  # Espacios y tabs
            (?P<NEWLINE>   \r?\n )                                      |  # Nueva línea
            (?P<COMMENT>   \#[^\n]* )                                   |  # Comentarios Python
            (?P<STRING>    (?:'''(?:[^'\\]|\\.|'(?!''))*''') |             # String triple comilla simple
                          (?:\"\"\"(?:[^\"\\]|\\.|\"(?!\"\"))*\"\"\")   |  # String triple comilla doble
                          (?:'(?:[^'\\]|\\.)*') |                          # String comilla simple
                          (?:\"(?:[^\"\\]|\\.)*\") )                       # String comilla doble
            (?P<FLOAT>     (?:[0-9]*\.[0-9]+)|(?:[0-9]+\.) )            |  # Float literals
            (?P<INT>       [0-9]+ )                                     |  # Integer literals
            (?P<KEYWORD>   \b(?:{kw_alt})\b )                           |  # Keywords
            (?P<ID>        [A-Za-z_][A-Za-z0-9_]* )                     |  # Identifiers
            (?P<OP>        (?:{op_alt}) )                               |  # Operators
            (?P<PUNCT>     (?:{punct_alt}) )                               # Punctuation
        """
