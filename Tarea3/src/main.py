from lexer.lexer_engine import Lexer, Token

def test_lexer_with_fortran_code():
    # Ejemplo de código Fortran 77
    fortran_code = """
      PROGRAM fchh
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
    lexer = Lexer(fortran_code)
    
    for token in lexer.tokens():
        print(token)

def test_lexer_from_file():
    """Función para leer código Fortran desde un archivo"""
    try:
        # Cambia esta ruta por la de tu archivo Fortran
        file_path = input("Ingresa la ruta del archivo Fortran (.f o .for): ").strip()
        
        with open(file_path, 'r', encoding='utf-8') as file:
            fortran_code = file.read()
        
        print(f"=== CÓDIGO DESDE ARCHIVO: {file_path} ===")
        print(fortran_code)
        print("\n=== ANÁLISIS LÉXICO ===")
        
        lexer = Lexer(fortran_code)
        
        tokens = list(lexer.tokens())
        
        # Mostrar estadísticas
        print(f"\nTotal de tokens: {len(tokens)}")
        
        # Contar por categorías
        categories = {}
        for token in tokens:
            cat = token.category.value
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nTokens por categoría:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")
        
        print("\nTodos los tokens:")
        for token in tokens:
            print(token)
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{file_path}'")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def test_specific_fortran_elements():
    """Prueba elementos específicos de Fortran 77"""
    test_cases = [
        ("Comentarios", "C Esto es un comentario\n* Otro comentario\n! Comentario moderno"),
        ("Etiquetas", "10    CONTINUE\n100   FORMAT(I5)\n9999  STOP"),
        ("Tipos de datos", "INTEGER I\nREAL X\nDOUBLE PRECISION Y\nLOGICAL FLAG\nCHARACTER*10 STR"),
        ("Literales", "123\n3.14\n2.5E-3\n1.23D-4\n.TRUE.\n.FALSE.\n'cadena'\n\"otra cadena\""),
        ("Operadores", "A = B + C * D ** 2\nIF (X .EQ. Y .AND. Z .GT. 0) THEN"),
        ("Estructuras de control", "IF (X .GT. 0) THEN\n   Y = X\nELSE\n   Y = -X\nENDIF"),
    ]
    
    for title, code in test_cases:
        print(f"\n=== {title} ===")
        print(f"Código: {repr(code)}")
        print("Tokens:")
        
        lexer = Lexer(code)
        for token in lexer.tokens():
            if token.category.value != "EOF":
                print(f"  {token}")

def main():
    print("LEXER PARA FORTRAN 77")
    print("====================")
    
    while True:
        print("\nOpciones:")
        print("1. Probar con código de ejemplo")
        print("2. Cargar archivo Fortran")
        print("3. Probar elementos específicos")
        print("4. Salir")
        
        choice = input("\nSelecciona una opción (1-4): ").strip()
        
        if choice == "1":
            test_lexer_with_fortran_code()
        elif choice == "2":
            test_lexer_from_file()
        elif choice == "3":
            test_specific_fortran_elements()
        elif choice == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, selecciona 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()