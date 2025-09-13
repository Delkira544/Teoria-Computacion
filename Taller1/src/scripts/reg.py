import re

def compilar_regex(patron: str, case_sensitive: bool):
    """
    Compila la expresión regular con el flag adecuado.
    Permite validar correos según configuración.
    """
    try:
        flags = 0 if case_sensitive else re.IGNORECASE
        return re.compile(patron, flags), flags
    except re.error as e:
        print(f"Error al compilar la expresión regular: {e}")
        return None, None


def probar_regex(patron: str, case_sensitive: bool, cadena: str):
    """
    Prueba si la cadena coincide con la expresión regular.
    Útil para testear el patrón antes de validar todo.
    """
    regex, _ = compilar_regex(patron, case_sensitive)
    if regex:
        return bool(regex.fullmatch(cadena))
    return False


def extraer_año(correo: str):
    """
    Extrae el año de la parte local del correo.
    """
    match = re.search(r'[0-9]{4}@', correo)
    if match:
        return match.group(0)[:-1]  # Elimina el @ al final
    return None


def validar_año_rango(año: str):
    """
    Valida que el año esté en el rango permitido.
    """
    try:
        año_num = int(año)
        return 2010 <= año_num <= 2025
    except (ValueError, TypeError):
        return False


def analizar_motivo(correo: str):
    """
    Analiza el motivo por el cual un correo es inválido.
    Realiza verificaciones secuenciales sobre el formato:
    - Vacío o espacios
    - Formato nombre[sep]apellido
    - Año de ingreso (4 dígitos antes del @)
    - Dominio correcto
    - Año en rango permitido
    Devuelve un string explicativo para mostrar al usuario.
    Si cambian las reglas, adaptar aquí los chequeos.
    """
    """
    Devuelve el motivo de invalidez según reglas del taller.
    Explica por qué un correo no es válido.
    """
    # Verificar si la línea está vacía
    if not correo.strip():
        return "línea vacía"
        
    # Verificar formato básico de nombre[separador]apellido
    if not re.match(r"^[a-zA-Z]+[._-][a-zA-Z]+", correo):
        if not re.match(r"^[a-zA-Z]+", correo):
            return "falta nombre"
        elif not re.search(r"[._-]", correo):
            return "falta separador (._-)"
        else:
            return "falta apellido"
    
    # Verificar que tenga 4 dígitos antes del @
    año_match = re.search(r"[0-9]{4}@", correo)
    if not año_match:
        if not re.search(r"@", correo):
            return "falta arroba (@)"
        elif re.search(r"[0-9]+@", correo):
            return "año debe tener exactamente 4 dígitos"
        else:
            return "falta año (4 dígitos)"
    
    # Verificar el dominio
    if not re.search(r"@techsolutions\.cl$", correo):
        return "dominio incorrecto, debe ser @techsolutions.cl"
    
    # Si el formato básico es correcto, verificar el rango del año
    año = extraer_año(correo)
    if año and not validar_año_rango(año):
        return f"año {año} fuera del rango permitido (2010-2025)"
    
    # Si llega aquí, hay algún otro problema con el formato
    return "no cumple con el formato requerido"


def validar_lineas(lineas, regex, case_sensitive: bool):
    """
    Valida cada línea de correo usando la expresión regular y reglas adicionales.
    Para cada línea:
    - Elimina espacios
    - Usa regex para formato general
    - Verifica año en rango
    - Si no es válido, llama a analizar_motivo para diagnóstico
    Devuelve lista de tuplas: (número de línea, correo, estado, motivo)
    """
    """Valida todas las líneas y retorna lista de resultados."""
    resultados = []
    for i, correo in enumerate(lineas, 1):
        # Eliminar espacios en blanco al inicio y final
        correo = correo.strip()
        
        if not correo:
            resultados.append((i, correo, "Inválido", "línea vacía"))
            continue
        
        # Validar formato básico con regex
        m = regex.fullmatch(correo)
        if m:
            # Si el formato básico es correcto, verificar el rango del año
            año = extraer_año(correo)
            if validar_año_rango(año):
                resultados.append((i, correo, "Válido", ""))
            else:
                resultados.append((i, correo, "Inválido", f"año {año} fuera del rango (2010-2025)"))
        else:
            motivo = analizar_motivo(correo)
            resultados.append((i, correo, "Inválido", motivo))
    
    return resultados


def generar_estadisticas(resultados):
    """
    Genera estadísticas a partir de los resultados de validación.
    Calcula total, válidos, inválidos y agrupa motivos de error.
    Útil para mostrar resumen en la interfaz.
    """
    """Genera estadísticas de validación."""
    total = len(resultados)
    validos = sum(1 for r in resultados if r[2] == "Válido")
    invalidos = total - validos
    
    # Agrupar motivos de invalidez
    motivos = {}
    for r in resultados:
        if r[2] == "Inválido":
            motivo = r[3]
            motivos[motivo] = motivos.get(motivo, 0) + 1
    
    # Calcular precisión si hay casos de prueba con resultados esperados
    precision = (validos / total * 100) if total > 0 else 0
    
    return {
        "total": total,
        "validos": validos,
        "invalidos": invalidos,
        "precision": precision,
        "motivos": motivos
    }
