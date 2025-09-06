# Manual de Instrucciones - Analizador Léxico con Interfaz Gráfica

## Descripción General

Esta aplicación es un analizador léxico (lexer) con interfaz gráfica desarrollada en Python usando Tkinter. Permite seleccionar archivos de código fuente, visualizar su contenido y analizar los tokens que contiene de manera organizada y detallada.

## Arquitectura del Proyecto

### Estructura de Directorios

```
├── src/                      # Código fuente principal
│   ├── main.py               # Punto de entrada de la aplicación
│   ├── gui/                  # Módulos de interfaz gráfica
│   │   ├── main_window.py    # Ventana principal
│   │   ├── file_selector.py  # Selector de archivos
│   │   └── token_display.py  # Visualizador de tokens
│   ├── lexer/                # Motor de análisis léxico
│   │   └── lexer_engine.py   # Lógica de tokenización
│   └── utils/                # Utilidades
│       └── file_handler.py   # Manejo de archivos
├── recurso.src               # Archivo de ejemplo
└── README.md                 # Esta documentación
```

## Componentes del Sistema

### 1. main.py

**Función**: Punto de entrada de la aplicación

- Inicializa la aplicación Tkinter
- Crea la ventana principal con el título "Lexer GUI"
- Ejecuta el bucle principal de la aplicación

### 2. gui/main_window.py

**Función**: Ventana principal de la aplicación

**Características**:
- Interfaz de 600x400 píxeles
- Botón "Select File" para seleccionar archivos
- Área de texto para mostrar el contenido del archivo
- Área separada para mostrar los tokens extraídos
- Barras de desplazamiento integradas
- Soporte para archivos `.src` y todos los tipos de archivo

### 3. gui/file_selector.py

**Función**: Componente especializado de selección de archivos

**Características**:
- Diálogo de selección de archivos
- Filtros para tipos python
- Visualización inmediata del contenido seleccionado
- Interfaz independiente reutilizable

### 4. gui/token_display.py

**Función**: Visualización avanzada de contenido y tokens

**Características**:
- Doble panel: contenido original y tokens
- Análisis automático al cargar archivo
- Integración directa con el motor léxico
- Formato detallado de tokens con posición

### 5. lexer/lexer_engine.py

**Función**: Motor de análisis léxico completo

**Características principales**:

#### Categorías de Tokens
- `KEYWORD`: Palabras clave de Python
- `IDENT`: Identificadores (variables, funciones)
- `LIT_INT`: Literales enteros
- `LIT_FLOAT`: Literales de punto flotante
- `LIT_STRING`: Cadenas de texto (simple, doble, triple)
- `OPERATOR`: Operadores aritméticos, lógicos y de asignación
- `PUNCT`: Puntuación (paréntesis, llaves, comas, etc.)
- `EOF`: Fin de archivo
- `ERROR`: Tokens no reconocidos

#### Registro de Tokens (TokenRegistry)
- **33 palabras clave** de Python incluidas
- **19 operadores** soportados (aritméticos, asignación, comparación)
- **10 símbolos de puntuación**
- Construcción automática de patrones regex optimizados

#### Expresiones Regulares Avanzadas
- Reconocimiento de strings con escape sequences
- Soporte para strings de triple comilla
- Comentarios Python (`# comentario`)
- Manejo de espacios en blanco y nuevas líneas
- Números enteros y flotantes

### 6. utils/file_handler.py

**Función**: Utilidades para manejo de archivos

- [`read_file_utf8`](Tarea2_2/src/utils/file_handler.py): Lee archivos con codificación UTF-8
- [`save_file_utf8`](Tarea2_2/src/utils/file_handler.py): Guarda archivos con codificación UTF-8
- Manejo robusto de errores de E/O

## Flujo de Funcionamiento

### 1. Inicio de la Aplicación

```bash
cd Tarea2_2
python src/main.py
```

### 2. Proceso de Análisis

1. **Selección de Archivo**: Click en "Select File"
2. **Carga**: El archivo se lee usando [`read_file_utf8`](Tarea2_2/src/utils/file_handler.py)
3. **Visualización**: Contenido mostrado en área de texto superior
4. **Análisis**: El [`Lexer`](Tarea2_2/src/lexer/lexer_engine.py) procesa automáticamente
5. **Resultados**: Tokens mostrados con información detallada

### 3. Formato de Salida de Tokens

Cada [`Token`](Tarea2_2/src/lexer/lexer_engine.py) incluye:

```
KEYWORD:IMPORT 'import' (1:1)
IDENT:IDENT 're' (1:8)
LIT_STRING:LIT_STRING '"var1 = 42 + 3.14;"' (3:8) value=var1 = 42 + 3.14;
```

- **Categoría**: Tipo general del token
- **Tipo específico**: Subtipo detallado
- **Lexema**: Texto original
- **Posición**: (línea:columna)
- **Valor**: Valor procesado (opcional)

## Tokens Reconocidos

### Palabras Clave de Python (33 total)
```python
"and", "or", "not", "if", "elif", "else", "while", "for", "in",
"def", "return", "pass", "class", "import", "from", "as",
"try", "except", "finally", "with", "lambda",
"True", "False", "None", "break", "continue",
"is", "del", "global", "nonlocal"
```

### Operadores (19 tipos)
- **Aritméticos**: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- **Asignación**: `=`, `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`
- **Comparación**: `==`, `!=`, `<`, `>`, `<=`, `>=`

### Puntuación (10 símbolos)
- **Agrupación**: `(`, `)`, `[`, `]`, `{`, `}`
- **Separadores**: `,`, `:`, `;`, `.`

### Literales
- **Enteros**: `123`, `0`, `999`
- **Flotantes**: `3.14`, `0.5`, `2.`
- **Strings**: `'texto'`, `"texto"`, `'''texto'''`, `"""texto"""`

## Instrucciones de Uso

### Requisitos
- Python 3.6 o superior
- Tkinter (incluido con Python estándar)

### Instalación y Ejecución

1. **Clonar/Descargar el proyecto**
2. **Navegar al directorio**:
   ```bash
   cd /ruta/a/Tarea2_2
   ```
3. **Ejecutar**:
   ```bash
   python src/main.py
   ```

### Uso de la Interfaz

1. **Abrir archivo**: Click en "Select File"
2. **Seleccionar**: Elegir archivo `.src` o cualquier archivo de texto
3. **Revisar contenido**: Panel superior muestra el código original
4. **Analizar tokens**: Panel inferior muestra análisis léxico completo

### Archivos de Ejemplo

El proyecto incluye [`recurso.src`](Tarea2_2/recurso.src) con código Python de ejemplo:

```python
import re

texto = "var1 = 42 + 3.14;"

for match in get_token(texto):
    tipo = match.lastgroup
    valor = match.group()
    if tipo != 'SKIP':
        print(f'{tipo}: {valor}')
```

## Características Técnicas Avanzadas

### Motor Léxico

- **Regex optimizada**: Patrones compilados para máximo rendimiento
- **Precedencia de operadores**: Manejo correcto de `**` vs `*`
- **Escape sequences**: Soporte completo para `\n`, `\t`, `\"`, etc.
- **Posicionamiento preciso**: Tracking de línea y columna
- **Manejo de errores**: Tokens inválidos marcados como ERROR

### Interfaz Gráfica

- **Responsive**: Redimensionamiento automático
- **Scrollbars**: Navegación fluida en archivos grandes  
- **Separación clara**: Paneles independientes para contenido y análisis
- **Feedback inmediato**: Análisis en tiempo real al seleccionar archivo

## Extensibilidad

### Agregar Nuevas Categorías

Modifica [`Category`](Tarea2_2/src/lexer/lexer_engine.py) enum:

```python
class Category(Enum):
    # ... existentes ...
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
```

### Agregar Nuevos Tokens

Actualiza [`TokenRegistry`](Tarea2_2/src/lexer/lexer_engine.py):

```python
self.keywords["new_keyword"] = "NEW_KEYWORD"
self.operators["<=>"] = "SPACESHIP"
```

### Personalizar Regex

Modifica [`build_regex_pattern`](Tarea2_2/src/lexer/lexer_engine.py) en TokenRegistry.

## Manejo de Errores

- **Archivos no encontrados**: Mensajes de error claros
- **Codificación**: Automática detección UTF-8
- **Tokens inválidos**: Marcados como ERROR con posición exacta
- **Archivos grandes**: Interfaz responsiva con scrollbars

## Notas Técnicas

- **Lenguaje**: Python 3.6+
- **GUI Framework**: Tkinter (estándar)
- **Regex Engine**: Módulo `re` de Python
- **Codificación**: UTF-8
- **Compatibilidad**: Multiplataforma (Linux, Windows, macOS)
- **Dependencias**: Solo bibliotecas estándar de Python

## Casos de Uso

1. **Educativo**: Aprender análisis léxico y compiladores
2. **Desarrollo**: Depurar analizadores léxicos
3. **Investigación**: Analizar patrones en código fuente
4. **Prototipado**: Base para analizadores más complejos

Este manual proporciona toda la información necesaria para entender, usar, extender y mantener la aplicación de análisis léxico.
