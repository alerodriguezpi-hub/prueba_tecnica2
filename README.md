# API REST para la Gestión de Datos Meteorológicos Ambientales

Este repositorio contiene la solución a la **Prueba Técnica - Convocatoria 4**, enfocada en el diseño, desarrollo e implementación de una API REST robusta para la ingesta, consulta, persistencia y análisis de datos meteorológicos e hidrológicos con frecuencia cincominutal.

---

## Arquitectura y Tecnologías Utilizadas

Para garantizar un rendimiento eficiente, alta escalabilidad y un estricto cumplimiento del estándar REST, el sistema se construyó bajo la siguiente pila tecnológica:

* **Framework Principal:** `FastAPI` (Python), seleccionado por su alto rendimiento, validación nativa de datos en tiempo de ejecución y generación automática de documentación interactiva.
* **Capa de Persistencia (ORM):** `SQLAlchemy`, implementando un enfoque de mapeo objeto-relacional para interactuar de forma segura con la base de datos mediante sesiones controladas.
* **Motor de Base de Datos:** `SQLite`, utilizado como motor relacional embebido local para facilitar la portabilidad, configurado bajo estrictas restricciones de llaves foráneas (`Foreign Keys`) e índices cronológicos.
* **Validación de Datos:** `Pydantic v2`, asegurando que cada payload de entrada y salida cumpla rigurosamente con los esquemas de tipado definidos.
* **Procesamiento de Datos Masivos:** `Pandas`, utilizado para la limpieza, parsing de marcas de tiempo Unix/estándar e ingesta masiva inicial a partir de los archivos de origen.



Diseño Relacional de la Base de Datos

Se optó por una arquitectura de base de datos normalizada para mitigar la redundancia de datos y optimizar los tiempos de consulta mediante la indexación estratégica:

1. Tabla `estaciones`:** Almacena los metadatos de los puntos de monitoreo ambiental identificados por un código único estructurado.
2. Tabla `mediciones`:** Almacena las lecturas de las variables meteorológicas (precipitación, temperatura, humedad, velocidad y dirección del viento, etc.). Mantiene una relación de cardinalidad `1:N` respecto a la tabla de estaciones mediante una restricción de llave foránea (`estacion_id`), garantizando la integridad referencial.

> **Optimización:** El campo `timestamp` (fecha y hora unificadas) cuenta con una restricción de unicidad (`unique=True`) e índice activo (`index=True`) para prevenir colisiones de datos cincominutales y acelerar exponencialmente las consultas de rangos históricos.

---

##  Instrucciones de Instalación y Despliegue Local

Siga los pasos descritos a continuación para configurar el entorno de ejecución en su máquina local:

### 1. Clonar el Repositorio e Ingresar al Directorio
```bash
git clone [https://github.com/alerodriguezpi-hub/prueba_tecnica2.git](https://github.com/alerodriguezpi-hub/prueba_tecnica2.git)
cd prueba_tecnica2

### 2. Configurar Entorno Virtual
Bash
# En macOS / Linux
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt

### 4. Inicializacion masiva de datos
python -m app.load_data

### 5. Levantar el servidor de aplicaciones
uvicorn app.main:app --reload