from lexer import Lexer, TokenRegistry, Parser

fortran_code = """
      PROGRAM CALC
      INTEGER X
      INTEGER Y
      REAL Z
      X = 10
      Y = 5
      Z = X + Y * 2
      IF (Z .GT. 15) THEN
          X = X + 1
      ENDIF
      END
"""

# 1. Configuración del Lexer (usando las clases de tu código original)
registry = TokenRegistry()
lexer = Lexer(fortran_code, registry)
lexer.recompile_pattern() # Recompilar el patrón regex si se añadieron ops/keywords

# 2. Ejecución del Parser
try:
    parser = Parser(lexer)
    result = parser.parse_programa()
    print(result)

except SyntaxError as e:
    print(f"\n¡FALLA DE PARSEO! Error: {e}")