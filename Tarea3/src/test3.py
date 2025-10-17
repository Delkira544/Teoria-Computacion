from lexer import LL1Parser, Lexer, TokenRegistry, Parser


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

registry = TokenRegistry()
lexer = Lexer(fortran_code, registry)
lexer.recompile_pattern()  # Recompilar el patrón regex si se añadieron ops/keywords


try:
    ll1_parser = LL1Parser(lexer)
    result = ll1_parser.parse()
    print(result)
except SyntaxError as e:
    print(f"\n¡FALLA DE PARSEO LL(1)! Error: {e}")

