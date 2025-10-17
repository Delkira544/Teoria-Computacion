from .lexer_engine import Lexer, Token, Category

# Definición de las producciones como tuplas
# P1: <programa> -> PROGRAM ID <bloque_declaraciones> <bloque_ejecutable> END
P1 = ("PROGRAM", "ID", "<bloque_declaraciones>", "<bloque_ejecutable>", "END")
# D1: <declaracion> -> INTEGER ID
D1 = ("INTEGER", "ID")
# A1: <asignacion> -> ID ASSIGN <expresion>
A1 = ("ID", "ASSIGN", "<expresion>")
# S1: <sentencia> -> <asignacion>
S1 = ("<asignacion>",)
# S2: <sentencia> -> <condicional>
S2 = ("<condicional>",)
# ... y así sucesivamente para todas las reglas.

# -----------------
# Tabla LL(1) M (Fragmento)
# -----------------
PARSING_TABLE = {
    "<programa>": {
        "PROGRAM": P1, 
        # EOF es necesario al inicio.
    },
    "<declaracion>": {
        "INTEGER": D1,
        "REAL": ("REAL", "ID"),
        # Regla de épsilon para terminar declaraciones. 
        # FOLLOW(<declaracion>) es {ID, IF, END}
        "ID": tuple(),   # Regla de épsilon (vacía)
        "IF": tuple(),   # Regla de épsilon
        "END": tuple(),  # Regla de épsilon
    },
    "<sentencia>": {
        "ID": S1,  # Si empieza con ID, es una asignación
        "IF": S2,  # Si empieza con IF, es un condicional
    },
    # ... más No Terminales
}


class LL1Parser:
    def __init__(self, lexer: Lexer, table: dict = PARSING_TABLE):
        self.token_stream = lexer.tokens()
        self.lookahead = next(self.token_stream)
        self.parsing_table = table
        # Pila inicializada con el símbolo inicial y EOF
        self.stack = ["EOF", "<programa>"]

    def parse(self):
        while self.stack:
            X = self.stack[-1]
            a = self.lookahead.kind

            if X == "EOF" and a == "EOF":
                print("\nAnálisis LL(1) completado con éxito.")
                return

            if X in PARSING_TABLE:  # X es un No Terminal (V)
                if a in self.parsing_table[X]:
                    production = self.parsing_table[X][a]
                    self.stack.pop() # POP a X
                    
                    # PUSH de la producción en orden inverso
                    if production: # Si no es épsilon
                        for symbol in reversed(production):
                            self.stack.append(symbol)
                    
                    print(f"Aplicada Regla {X} -> {production} con lookahead {a}")

                else:
                    raise SyntaxError(f"Error LL(1): No hay producción para M[{X}, {a}]")

            elif X == a:  # X es un Terminal (Σ)
                self.stack.pop()
                print(f"Consumido Terminal: {X} ('{self.lookahead.lexeme}')")
                
                # Avanzar el lookahead
                try:
                    self.lookahead = next(self.token_stream)
                except StopIteration:
                    self.lookahead = Token(Category.EOF, "EOF", "", 0, 0)
            
            else: # X es un Terminal, pero no coincide con a
                raise SyntaxError(f"Error LL(1): Esperado '{X}' pero encontrado '{a}'")
