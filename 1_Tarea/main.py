from dataclasses import dataclass

class Tarjeta:
    id_tarjeta: str
    titular: str
    def __init__(self, id_tarjeta: str, titular: str) -> None:
        self.id_tarjeta = id_tarjeta
        self.titular = titular


class Torniquete:
    def __init__(self) -> None:
        self.activo = False 

    def activar(self) -> None:
        self.activo = True

    def desactivar(self) -> None:
        self.activo = False

    def __repr__(self) -> str:
        return f"Torniquete esta activo={self.activo}"


class Sistema:
    def __init__(self) -> None:
        self._usuarios: dict[str, str] = {}    # id_tarjeta -> pin (str de 4 dígitos)
        self._bloqueado: bool = False
        self._fallos_consecutivos: int = 0
        self.torniquete = Torniquete()

    @staticmethod
    def _validar_pin(pin: str) -> None:
        if not (len(pin) == 4 and pin.isdigit()):
            raise ValueError("El PIN debe ser una cadena de 4 dígitos (0-9)")

    def registrar_usuario(self, tarjeta: Tarjeta, pin: str) -> None:
        self._validar_pin(pin)
        self._usuarios[tarjeta.id_tarjeta] = pin

    def esta_bloqueado(self) -> bool:
        return self._bloqueado

    def autenticar(self, tarjeta: Tarjeta, pin_ingresado: str) -> bool:
        if self._bloqueado:
            self.torniquete.desactivar()
            print("Sistema bloqueado")
            return False
        self._validar_pin(pin_ingresado)

        pin_registrado = self._usuarios.get(tarjeta.id_tarjeta)
        if pin_registrado is None:
            self._registrar_fallo()
            self.torniquete.desactivar()
            print("Tarjeta no reconocida - Acceso denegado")
            return False

        if pin_ingresado == pin_registrado:
            self._fallos_consecutivos = 0
            self.torniquete.activar()
            print(f"Acceso concedido a {tarjeta.titular} - Torniquete activado")
            return True
        else:
            self._registrar_fallo()
            self.torniquete.desactivar()
            intentos_restantes = max(0, 3 - self._fallos_consecutivos)
            if self._bloqueado:
                print("PIN incorrecto - Sistema Bloqueado")
            else:
                print(f"PIN incorrecto - ntentos restantes: {intentos_restantes}")
            return False

    def _registrar_fallo(self) -> None:
        self._fallos_consecutivos += 1
        if self._fallos_consecutivos >= 3:
            self._bloqueado = True

    def __repr__(self) -> str:
        estado = "BLOQUEADO" if self._bloqueado else "OPERATIVO"
        return f"Sistema(estado={estado}, fallos={self._fallos_consecutivos}, {self.torniquete})"


if __name__ == "__main__":
    # Crear sistema y registrar usuarios
    sistema = Sistema()
    tarjeta_ana = Tarjeta(id_tarjeta="T-001", titular="Ana Pérez")
    tarjeta_luis = Tarjeta(id_tarjeta="T-002", titular="Luis Soto")

    sistema.registrar_usuario(tarjeta_ana, "1234")
    sistema.registrar_usuario(tarjeta_luis, "9876")

    # Simulación: Ana intenta entrar con distintos PINs
    print(sistema)
    sistema.autenticar(tarjeta_ana, "0000")  # fallo 1
    print(sistema)
    sistema.autenticar(tarjeta_ana, "1111")  # fallo 2
    print(sistema)
    sistema.autenticar(tarjeta_ana, "2222")  # fallo 3 -> bloquea
    print(sistema)

    # Aunque ahora use el PIN correcto, el sistema está bloqueado
    sistema.autenticar(tarjeta_ana, "1234")
    print(sistema)

    # Intento exitoso
    sistema.autenticar(tarjeta_ana, "1234")
    print(sistema)

    # Tarjeta no registrada (cuenta como fallo)
    tarjeta_fake = Tarjeta(id_tarjeta="T-999", titular="Intruso")
    sistema.autenticar(tarjeta_fake, "0000")
    print(sistema)
