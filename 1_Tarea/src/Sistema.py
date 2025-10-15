from src.Tarjeta import Tarjeta
from abc import ABC, abstractmethod

# Principio de Responsabilidad Única: Cada estado tiene una sola responsabilidad
class Estado(ABC):
    @abstractmethod
    def ingresar_tarjeta(self, sistema, tarjeta):
        pass
    
    @abstractmethod
    def ingresar_clave(self, sistema, clave):
        pass

# Estado: Esperando Tarjeta (Estado inicial)
class EsperandoTarjeta(Estado):
    def ingresar_tarjeta(self, sistema, tarjeta):
        if tarjeta in sistema.tarjetas_permitidas:
            sistema.tarjeta_actual = tarjeta
            print("Tarjeta reconocida. Ingrese su clave.")
            sistema.cambiar_estado(EsperandoClave())
        else:
            print("Tarjeta no permitida. Acceso denegado.")
    
    def ingresar_clave(self, sistema, clave):
        print("Primero debe ingresar una tarjeta válida.")

# Estado: Esperando Clave
class EsperandoClave(Estado):
    def ingresar_tarjeta(self, sistema, tarjeta):
        print("Ya hay una tarjeta en proceso. Complete la autenticación.")
    
    def ingresar_clave(self, sistema, clave):
        if sistema.validar_clave(sistema.tarjeta_actual, clave):
            print("Código correcto. Acceso permitido.")
            sistema.cambiar_estado(AccesoPermitido())
        else:
            print("Código incorrecto. Primer intento fallido.")
            sistema.cambiar_estado(PrimerIntentoEsperandoClave())

# Estado: Primer Intento Esperando Clave
class PrimerIntentoEsperandoClave(Estado):
    def ingresar_tarjeta(self, sistema, tarjeta):
        print("Complete la autenticación actual o reinicie el sistema.")
    
    def ingresar_clave(self, sistema, clave):
        if sistema.validar_clave(sistema.tarjeta_actual, clave):
            print("Código correcto. Acceso permitido.")
            sistema.cambiar_estado(AccesoPermitido())
        else:
            print("Código incorrecto. Segundo intento fallido.")
            sistema.cambiar_estado(SegundoIntentoEsperandoClave())

# Estado: Segundo Intento Esperando Clave
class SegundoIntentoEsperandoClave(Estado):
    def ingresar_tarjeta(self, sistema, tarjeta):
        print("Complete la autenticación actual o el sistema será bloqueado.")
    
    def ingresar_clave(self, sistema, clave):
        if sistema.validar_clave(sistema.tarjeta_actual, clave):
            print("Código correcto. Acceso permitido.")
            sistema.cambiar_estado(AccesoPermitido())
        else:
            print("Código incorrecto. Sistema bloqueado por seguridad.")
            sistema.cambiar_estado(SistemaBloqueado())

# Estado: Acceso Permitido
class AccesoPermitido(Estado):
    def ingresar_tarjeta(self, sistema, tarjeta):
        print("Acceso ya concedido. Retire la tarjeta para reiniciar el sistema.")
        sistema.reiniciar()
    
    def ingresar_clave(self, sistema, clave):
        print("Acceso ya concedido. Retire la tarjeta para continuar.")

# Estado: Sistema Bloqueado
class SistemaBloqueado(Estado):
    def ingresar_tarjeta(self, sistema, tarjeta):
        print("Sistema bloqueado por seguridad. Contacte al administrador.")
    
    def ingresar_clave(self, sistema, clave):
        print("Sistema bloqueado. No se pueden ingresar claves.")

# Principio de Inversión de Dependencias: Sistema depende de abstracciones (Estado)
# Principio Abierto/Cerrado: Abierto para extensión (nuevos estados), cerrado para modificación
class Sistema:
    def __init__(self):
        self.tarjetas_permitidas = {}  # {tarjeta: clave}
        self.estado = EsperandoTarjeta()
        self.tarjeta_actual = None

    def cambiar_estado(self, nuevo_estado: Estado):
        self.estado = nuevo_estado

    def agregar_tarjeta(self, tarjeta: Tarjeta, clave: str):
        """Registra una tarjeta con su clave correspondiente"""
        self.tarjetas_permitidas[tarjeta] = clave
        print(f"Tarjeta {tarjeta.numero} agregada con éxito.")

    def validar_clave(self, tarjeta: Tarjeta, clave: str):
        """Valida si la clave ingresada corresponde a la tarjeta"""
        return self.tarjetas_permitidas.get(tarjeta) == clave

    def ingresar_tarjeta(self, tarjeta: Tarjeta):
        """Procesa el ingreso de una tarjeta"""
        self.estado.ingresar_tarjeta(self, tarjeta)

    def ingresar_clave(self, clave: str):
        """Procesa el ingreso de una clave"""
        self.estado.ingresar_clave(self, clave)

    def reiniciar(self):
        """Reinicia el sistema al estado inicial"""
        self.estado = EsperandoTarjeta()
        self.tarjeta_actual = None
        print("Sistema reiniciado. Esperando nueva tarjeta.")

    def desbloquear_sistema(self):
        """Permite al administrador desbloquear el sistema"""
        if isinstance(self.estado, SistemaBloqueado):
            self.reiniciar()
            print("Sistema desbloqueado por el administrador.")
        else:
            print("El sistema no está bloqueado.")

    def obtener_estado_actual(self):
        """Devuelve el nombre del estado actual"""
        return self.estado.__class__.__name__