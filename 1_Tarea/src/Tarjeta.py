class Tarjeta:
    def __init__(self, numero):
        self.numero = numero

    def __eq__(self, other):
        if isinstance(other, Tarjeta):
            return self.numero == other.numero
        return False
