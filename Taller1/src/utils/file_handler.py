import os


def cargar_archivo_txt(ruta):
    """Carga un archivo .txt y retorna las líneas útiles."""
    try:
        with open(ruta, encoding="utf-8") as f:
            lineas = [line.strip() for line in f.readlines()]
        if not any(lineas):
            return None, "El archivo no contiene líneas útiles."
        return lineas, None
    except Exception as e:
        return None, str(e)


def exportar_resultados(ruta, resultados):
    """Exporta los resultados a un archivo CSV/TXT."""
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("linea,correo,estado,motivo\n")
            for r in resultados:
                f.write(f"{r[0]},{r[1]},{r[2]},{r[3]}\n")
        return None
    except Exception as e:
        return str(e)


def read_file(filepath):
    """Lee el contenido de un archivo."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def save_file(filepath, content):
    """Guarda contenido en un archivo."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def file_exists(filepath):
    """Verifica si un archivo existe."""
    return os.path.exists(filepath)
