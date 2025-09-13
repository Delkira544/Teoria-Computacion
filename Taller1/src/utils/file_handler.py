import os


def cargar_archivo_txt(ruta):
    """
    Carga un archivo .txt y retorna las líneas útiles.
    Útil para leer correos desde archivo externo.
    """
    try:
        with open(ruta, encoding="utf-8") as f:
            lineas = [line.strip() for line in f.readlines()]
        if not any(lineas):
            return None, "El archivo no contiene líneas útiles."
        return lineas, None
    except Exception as e:
        return None, str(e)


def exportar_resultados(ruta, resultados):
    """
    Exporta los resultados a un archivo CSV/TXT.
    Permite guardar el reporte de validación.
    """
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("linea,correo,estado,motivo\n")
            for r in resultados:
                f.write(f"{r[0]},{r[1]},{r[2]},{r[3]}\n")
        return None
    except Exception as e:
        return str(e)


def read_file(filepath):
    """
    Lee el contenido completo de un archivo.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def save_file(filepath, content):
    """
    Guarda texto en un archivo.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def file_exists(filepath):
    """
    Verifica si un archivo existe en disco.
    """
    """Verifica si un archivo existe."""
    return os.path.exists(filepath)
