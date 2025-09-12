import re

def compilar_regex(patron: str, case_sensitive: bool):
    """Compila la expresión regular con el flag adecuado."""
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.compile(patron, flags), flags


def probar_regex(patron: str, case_sensitive: bool, cadena: str):
    """Prueba si la cadena coincide con la expresión regular."""
    regex, _ = compilar_regex(patron, case_sensitive)
    return bool(regex.fullmatch(cadena))


def analizar_motivo(correo: str, patron: str):
    """Devuelve el motivo de invalidez según reglas del taller."""
    # Adaptar aquí si cambian reglas
    if not re.match(r"^[a-zA-Z]+[._-][a-zA-Z]+", correo):
        return "separador o caracteres no permitidos"
    if not re.search(r"[0-9]{4}@", correo):
        return "no termina en 4 dígitos"
    if not re.search(r"@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo):
        return "dominio inválido"
    return "no cumple formato"


def validar_lineas(lineas, regex, patron):
    """Valida todas las líneas y retorna lista de resultados."""
    resultados = []
    for i, correo in enumerate(lineas, 1):
        if not correo or correo.isspace():
            resultados.append((i, correo, "Inválido", "línea vacía/espacios"))
            continue
        m = regex.fullmatch(correo)
        if m:
            resultados.append((i, correo, "Válido", ""))
        else:
            motivo = analizar_motivo(correo, patron)
            resultados.append((i, correo, "Inválido", motivo))
    return resultados
