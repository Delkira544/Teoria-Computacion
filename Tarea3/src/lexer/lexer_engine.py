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
    LIT_REAL = "LIT_REAL"
    LIT_STRING = "LIT_STRING"
    OPERATOR = "OPERATOR"
    PUNCT = "PUNCT"
    LABEL = "LABEL"
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
        val_str = f" = {self.value}" if self.value is not None else ""
        return (f"[{self.line}:{self.col}] {self.category.value:<14} "
                f"{self.kind:<10} '{self.lexeme}'{val_str}")

class TokenRegistry:
    def __init__(self):
        # Palabras clave más importantes de Fortran 77
        self.keywords: Dict[str, str] = {
            # Tipos de datos
            "integer": "INTEGER", "real": "REAL",  

            # Estructuras de control
            "if": "IF", "then": "THEN", "else": "ELSE", "endif": "ENDIF",
            
            # Subprogramas
            "program": "PROGRAM", "end": "END", 
            
            # Valores lógicos
            "true": "TRUE", "false": "FALSE",
        }
        
        # Operadores de Fortran 77
        self.operators: Dict[str, str] = {
            # Aritméticos
            "+": "PLUS", "-": "MINUS", "*": "MULT", "/": "DIV", "**": "POWER",
            # Relacionales
            ".eq.": "EQ", ".ne.": "NE", ".lt.": "LT", ".le.": "LE", 
            ".gt.": "GT", ".ge.": "GE",
            # Asignación
            "=": "ASSIGN",
        }
        
        # Puntuación
        self.punctuation: Dict[str, str] = {
            "(": "LPAREN", ")": "RPAREN",
            }

    def _create_alternation(self, symbols: list[str]) -> str:
        if not symbols:
            return r"(?!x)x"
        return "|".join(re.escape(s) for s in sorted(symbols, key=len, reverse=True))

    def build_regex_pattern(self) -> str:
        kw_alt = self._create_alternation(list(self.keywords.keys()))
        op_alt = self._create_alternation(list(self.operators.keys()))
        punct_alt = self._create_alternation(list(self.punctuation.keys()))

        return rf"""
            (?P<WS>        [ \t\r\n]+ )                        |  
            (?P<COMMENT>   ^[ \t]*[cC*][^\n]* )                |  
            (?P<LABEL>     ^[ \t]*[0-9]{{1,5}}[ \t]+ )         |
            (?P<KEYWORD>   \b(?i:{kw_alt})\b )                 |  
            (?P<ID>        [A-Za-z][A-Za-z0-9_]* )             |  
            (?P<REAL>      [0-9]+\.[0-9]*([eE][+-]?[0-9]+)?[dD]? |
                           [0-9]+[eE][+-]?[0-9]+[dD]? |
                           \.[0-9]+([eE][+-]?[0-9]+)?[dD]? )   |
            (?P<INT>       [0-9]+ )                            |  
            (?P<STRING>    '([^']|'')*' )                      |
            (?P<OP>        (?i:{op_alt}) )                     |  
            (?P<PUNCT>     (?:{punct_alt}) )                   
        """

class TokenFactory:
    def __init__(self, registry: TokenRegistry):
        self.registry = registry
        self._creators: Dict[str, Callable] = {
            "KEYWORD": self._create_keyword,
            "ID": self._create_identifier,
            "INT": self._create_integer,
            "REAL": self._create_real,
            "STRING": self._create_string,
            "OP": self._create_operator,
            "PUNCT": self._create_punctuation,
            "LABEL": self._create_label,
        }

    def create_token(self, token_type: str, lexeme: str, line: int, col: int) -> Token:
        creator = self._creators.get(token_type)
        if creator:
            return creator(lexeme, line, col)
        return self._create_error(lexeme, line, col)

    def _create_keyword(self, lexeme: str, line: int, col: int) -> Token:
        # Fortran es case-insensitive
        kind = self.registry.keywords[lexeme.lower()]
        return Token(Category.KEYWORD, kind, lexeme, line, col)

    def _create_identifier(self, lexeme: str, line: int, col: int) -> Token:
        return Token(Category.IDENT, "ID", lexeme, line, col)

    def _create_integer(self, lexeme: str, line: int, col: int) -> Token:
        return Token(Category.LIT_INT, "INT", lexeme, line, col, value=int(lexeme))

    def _create_real(self, lexeme: str, line: int, col: int) -> Token:
        # Manejo de notación científica y doble precisión
        clean_lexeme = lexeme.lower().replace('d', 'e')  # Double precision
        try:
            value = float(clean_lexeme)
        except ValueError:
            value = 0.0
        return Token(Category.LIT_REAL, "REAL", lexeme, line, col, value=value)

    def _create_string(self, lexeme: str, line: int, col: int) -> Token:
        # Remover comillas y manejar comillas dobles
        string_value = lexeme[1:-1].replace("''", "'")
        return Token(Category.LIT_STRING, "STRING", lexeme, line, col, value=string_value)

    def _create_operator(self, lexeme: str, line: int, col: int) -> Token:
        kind = self.registry.operators[lexeme.lower()]
        return Token(Category.OPERATOR, kind, lexeme, line, col)

    def _create_punctuation(self, lexeme: str, line: int, col: int) -> Token:
        kind = self.registry.punctuation[lexeme]
        return Token(Category.PUNCT, kind, lexeme, line, col)

    def _create_label(self, lexeme: str, line: int, col: int) -> Token:
        label_num = lexeme.strip()
        return Token(Category.LABEL, "LABEL", lexeme, line, col, value=int(label_num))

    def _create_error(self, lexeme: str, line: int, col: int) -> Token:
        return Token(Category.ERROR, "UNKNOWN_CHAR", lexeme, line, col)

class PositionTracker:
    def __init__(self, line: int = 1, col: int = 1):
        self.line = line
        self.col = col

    def advance(self, text: str) -> tuple[int, int]:
        start_line, start_col = self.line, self.col
        
        for char in text:
            if char == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
                
        return start_line, start_col

    def advance_single_char(self, char: str) -> tuple[int, int]:
        start_line, start_col = self.line, self.col
        
        if char == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
            
        return start_line, start_col

class Lexer:
    def __init__(self, text: str, registry: TokenRegistry | None = None):
        self.text = text
        self.pos = 0
        self.position_tracker = PositionTracker()
        
        self.registry = registry or TokenRegistry()
        self.token_factory = TokenFactory(self.registry)
        self.pattern = self._compile_pattern()

    def _compile_pattern(self) -> Pattern[str]:
        pattern_str = self.registry.build_regex_pattern()
        return re.compile(pattern_str, re.VERBOSE | re.MULTILINE)

    def recompile_pattern(self) -> None:
        self.pattern = self._compile_pattern()

    def tokens(self) -> Iterator[Token]:
        while self.pos < len(self.text):
            token = self._next_token()
            if token:
                yield token

        yield Token(Category.EOF, "EOF", "", 
                   self.position_tracker.line, self.position_tracker.col)

    def _next_token(self) -> Token | None:
        match = self.pattern.match(self.text, self.pos)
        
        if not match:
            return self._handle_unknown_character()

        token_type = match.lastgroup      
        lexeme = match.group(token_type)
        start_line, start_col = self.position_tracker.advance(lexeme)
        self.pos = match.end()

        if token_type in ("WS", "COMMENT"):
            return None

        return self.token_factory.create_token(token_type, lexeme, start_line, start_col)

    def _handle_unknown_character(self) -> Token:
        bad_char = self.text[self.pos]
        start_line, start_col = self.position_tracker.advance_single_char(bad_char)
        self.pos += 1
        
        return self.token_factory._create_error(bad_char, start_line, start_col)