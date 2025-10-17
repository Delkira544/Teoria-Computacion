# Asumimos que las clases Token, Category, Lexer, etc., están definidas.
from .lexer_engine import Lexer, Token, Category


class Parser:
    def __init__(self, lexer: Lexer):
        self.token_stream = lexer.tokens()
        self.current_token = next(self.token_stream)

    def consume(self, expected_kind: str) -> Token:
        """Comprueba y consume el token actual si coincide con el kind esperado."""
        if self.current_token.kind == expected_kind:
            consumed_token = self.current_token
            try:
                self.current_token = next(self.token_stream)
            except StopIteration:
                pass
            return consumed_token
        else:
            raise SyntaxError(
                f"Error Sintáctico: Esperado '{expected_kind}' pero encontrado "
                f"'{self.current_token.kind}' ('{self.current_token.lexeme}') "
                f"en [{self.current_token.line}:{self.current_token.col}]"
            )

    # -----------------------------------------------------------------
    # No Terminales (V) e Reglas de Producción (R)
    # -----------------------------------------------------------------
    
    # V: <programa>
    # R: PROGRAM ID <bloque_declaraciones> <bloque_ejecutable> END
    def parse_programa(self) -> str:
        self.consume("PROGRAM")
        program_name = self.consume("ID").lexeme
        print(f"\n[PARSEANDO PROGRAMA: {program_name}]")
        
        self.parse_bloque_declaraciones()
        self.parse_bloque_ejecutable()
        
        self.consume("END")
        self.consume("EOF")
        
        return f"\nPrograma '{program_name}' parseado con éxito."

    # V: <bloque_declaraciones>
    # R: <declaracion>*
    def parse_bloque_declaraciones(self):
        print("  [BLOQUE DE DECLARACIONES]")
        # Sigue parseando declaraciones mientras el token actual sea INTEGER o REAL
        while self.current_token.kind in ("INTEGER", "REAL"):
            self.parse_declaracion()
        print("  [FIN DECLARACIONES]")

    # V: <declaracion>
    # R: INTEGER ID | REAL ID
    def parse_declaracion(self):
        if self.current_token.kind == "INTEGER":
            type_token = self.consume("INTEGER")
        elif self.current_token.kind == "REAL":
            type_token = self.consume("REAL")
        else:
            raise SyntaxError("Esperado tipo (INTEGER o REAL).")
            
        var_name = self.consume("ID").lexeme
        print(f"    -> Declaración: {type_token.lexeme} {var_name}")


    # V: <bloque_ejecutable>
    # R: <sentencia>*
    def parse_bloque_ejecutable(self):
        print("  [BLOQUE EJECUTABLE]")
        # Las sentencias ejecutables comienzan con ID (asignación) o IF (condicional)
        while self.current_token.kind in ("ID", "IF"):
            self.parse_sentencia()
        print("  [FIN EJECUTABLE]")

    # V: <sentencia>
    # R: <asignacion> | <condicional>
    def parse_sentencia(self):
        if self.current_token.kind == "ID":
            self.parse_asignacion()
        elif self.current_token.kind == "IF":
            self.parse_condicional()
        else:
            raise SyntaxError("Esperado sentencia (Asignación o IF).")
            
    # V: <asignacion>
    # R: ID ASSIGN <expresion>
    def parse_asignacion(self) -> None:
        var_name = self.consume("ID").lexeme
        self.consume("ASSIGN")
        print(f"    -> Asignación: {var_name} = ...")
        self.parse_expresion()
        
    # V: <condicional>
    # R: IF LPAREN <expresion_logica> RPAREN THEN <bloque_ejecutable> ENDIF
    def parse_condicional(self):
        print("    -> Sentencia IF iniciada")
        self.consume("IF")
        self.consume("LPAREN")
        self.parse_expresion_logica()
        self.consume("RPAREN")
        self.consume("THEN")
        
        # Recursión: el bloque ejecutable dentro del IF
        self.parse_bloque_ejecutable() 
        
        self.consume("ENDIF")
        print("    -> Sentencia IF terminada")

    # V: <expresion_logica>
    # R: <expresion> REL_OP <expresion>
    def parse_expresion_logica(self):
        print("    -> Parseando Expresión Lógica...")
        self.parse_expresion()
        
        # Los operadores relacionales son terminales como EQ, GT, LE, etc.
        if self.current_token.kind in ("EQ", "NE", "LT", "LE", "GT", "GE"):
            op = self.consume(self.current_token.kind)
            print(f"    -> Operador Relacional: {op.lexeme}")
            self.parse_expresion()
        else:
            raise SyntaxError("Esperado operador relacional.")

    # V: <expresion> (Simplificado: soporta +, -, *, /)
    # R: <termino> ( (PLUS | MINUS | MULT | DIV) <expresion> )?
    def parse_expresion(self) -> None:
        self.parse_termino()
        
        if self.current_token.kind in ("PLUS", "MINUS", "MULT", "DIV"):
            op = self.consume(self.current_token.kind)
            # print(f"    -> Operador Aritmético: {op.lexeme}")
            self.parse_expresion()
            
    # V: <termino>
    # R: ID | INT | REAL
    def parse_termino(self) -> None:
        if self.current_token.kind in ("ID", "INT", "REAL"):
            value = self.consume(self.current_token.kind).lexeme
            # print(f"    -> Consumido término: {value}")
        else:
            raise SyntaxError("Esperado término (ID, INT, REAL).")