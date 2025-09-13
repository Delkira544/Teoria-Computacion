# Validador de Correos Electrónicos

## Descripción General

Esta aplicación permite validar correos electrónicos según un formato específico, utilizando expresiones regulares. Está diseñada principalmente para validar correos del dominio `techsolutions.cl` con un formato predefinido, pero es configurable para adaptarse a diferentes patrones.

## Requisitos

Para ejecutar la aplicación, necesitarás:

- Python 3.6 o superior
- Bibliotecas estándar de Python (incluidas en la instalación básica)
- Tkinter (generalmente incluido con Python)

## Cómo Ejecutar la Aplicación

1. Abre una terminal en la carpeta raíz del proyecto
2. Ejecuta el siguiente comando:

```bash
python main.py
```

## Características Principales

- **Validación de correos** según expresiones regulares personalizables
- **Carga de correos** desde archivos de texto
- **Visualización de resultados** con estadísticas detalladas
- **Exportación de resultados** en formatos TXT y CSV
- **Prueba interactiva** de expresiones regulares
- **Interfaz gráfica intuitiva** con pestañas de configuración y resultados

## Guía de Uso

### 1. Pestaña de Configuración

#### Carga de Archivo

1. Haz clic en el botón **Examinar...** para seleccionar un archivo TXT con los correos a validar
2. El contenido del archivo se mostrará en el área de texto

#### Configuración de Expresión Regular

1. En el campo **Patrón**, define la expresión regular para validar los correos
   - El patrón predeterminado es: `^[a-zA-Z]+[._-][a-zA-Z]+[0-9]{4}@techsolutions\.cl$`
   - Este patrón valida correos con formato: `nombre[._-]apellido####@techsolutions.cl`
2. Marca o desmarca la opción **Sensible a mayúsculas/minúsculas** según tus necesidades
3. Usa la sección **Probar Expresión Regular** para verificar cómo funciona tu patrón con ejemplos

#### Validación

1. Una vez configurado, haz clic en **Validar correos** para iniciar el proceso

### 2. Pestaña de Resultados

#### Visualización de Resultados

- La tabla muestra cada correo con su número de línea, estado (Válido/Inválido) y motivo de invalidez
- Puedes filtrar los resultados usando el desplegable **Filtrar** (Todos, Válidos, Inválidos)

#### Estadísticas

- En el panel derecho se muestran estadísticas detalladas:
  - Total de correos analizados
  - Cantidad de correos válidos e inválidos
  - Precisión (porcentaje de correos válidos)
  - Motivos de invalidez agrupados

#### Exportación

1. Haz clic en **Exportar** y selecciona el formato deseado (TXT o CSV)
2. Elige la ubicación donde guardar el archivo de resultados

## Reglas de Validación

Para que un correo sea válido debe cumplir:

1. Tener el formato: `nombre[separador]apellido####@techsolutions.cl`

   - El nombre y apellido deben contener solo letras (a-z, A-Z)
   - El separador puede ser punto (.), guion bajo (\_) o guion medio (-)
   - Debe tener exactamente 4 dígitos para el año
   - El dominio debe ser exactamente `techsolutions.cl`

2. El año debe estar entre 2010 y 2025 (inclusive)

## Estructura del Proyecto

```
.
├── main.py                    # Punto de entrada de la aplicación
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Documentación
└── src/                       # Código fuente
    ├── data/                  # Datos de ejemplo
    │   └── cadenas.txt        # Archivo de ejemplo con correos
    ├── scripts/               # Lógica de validación
    │   ├── __init__.py
    │   └── reg.py             # Funciones de validación con regex
    ├── ui/                    # Interfaz de usuario
    │   ├── __init__.py
    │   ├── components.py      # Componentes reutilizables de la UI
    │   └── main_window.py     # Ventana principal de la aplicación
    └── utils/                 # Utilidades
        ├── __init__.py
        └── file_handler.py    # Manejo de archivos
```

## Ejemplos de Correos Válidos e Inválidos

### Válidos

- `juan.perez2015@techsolutions.cl`
- `maria_lopez2020@techsolutions.cl`
- `carlos-rodriguez2010@techsolutions.cl`

### Inválidos

- `juan2015@techsolutions.cl` (falta separador y apellido)
- `juan.perez@techsolutions.cl` (faltan los 4 dígitos del año)
- `juan.perez2009@techsolutions.cl` (año fuera del rango permitido)
- `juan.perez2015@gmail.com` (dominio incorrecto)

## Solución de Problemas

- **La aplicación no arranca**: Verifica que tienes Python instalado y que estás ejecutando el comando desde la carpeta raíz del proyecto.
- **Error al cargar archivos**: Asegúrate de que el archivo existe y tiene permisos de lectura.
- **Resultados inesperados**: Revisa la expresión regular y considera si debe ser sensible a mayúsculas/minúsculas.
- **La interfaz no se muestra correctamente**: Asegúrate de tener Tkinter correctamente instalado con tu versión de Python.

## Desarrollo

La aplicación está estructurada en módulos:

- `main.py`: Punto de entrada que inicializa la aplicación
- `src/scripts/reg.py`: Contiene la lógica de validación de expresiones regulares
- `src/ui/main_window.py`: Define la ventana principal y la lógica de la interfaz
- `src/ui/components.py`: Componentes reutilizables de la interfaz
- `src/utils/file_handler.py`: Funciones para cargar y guardar
