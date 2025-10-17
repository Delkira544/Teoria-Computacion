import string
from lexer import Lexer, TokenRegistry, Parser




registry = TokenRegistry()

for i in string.ascii_uppercase:
    texto = f"PROGRAM {i}afasdfa"
    lexer = Lexer(texto, registry)

    print(i, end=": ")
    for token in lexer.tokens():
        print(token)
    
