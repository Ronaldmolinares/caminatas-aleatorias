# Caminatas Aleatorias - Simulación de Computadores

## Descripción del Proyecto

Este proyecto implementa simulaciones de **caminatas aleatorias** (random walks) en espacios de una, dos y tres dimensiones. Una caminata aleatoria es un proceso estocástico donde una partícula se desplaza en pasos aleatorios sucesivos, comúnmente modelado mediante un generador de números pseudoaleatorios.

El proyecto incluye:
- **Generador de números pseudoaleatorios** basado en el método de Congruencia Lineal
- **Caminatas aleatorias** en 1D, 2D y 3D con visualizaciones
- **Pruebas de validación** para garantizar la calidad de los números generados

## Estructura del Proyecto

```
caminatas-aleatorias/
├── una_dimension/              # Caminata aleatoria en 1D
│   ├── main.py
│   └── utils.py
├── dos_dimensiones/            # Caminata aleatoria en 2D
│   ├── main.py
│   └── utils.py
├── tres_dimensiones/           # Caminata aleatoria en 3D
│   ├── main.py
│   └── utils.py
├── generador_numeros/          # Generador de números pseudoaleatorios
│   └── congruencia_lineal.py
├── validacion_numeros/         # Pruebas de validación
│   ├── aleatoriedad.py         # Prueba de aleatoriedad
│   ├── uniformidad.py          # Prueba de uniformidad
│   └── no_correlacion_serial.py # Prueba de no correlación serial
└── prueba_dos_dimensiones/     # Pruebas específicas para 2D
    ├── main.py
    ├── generador.py
    ├── campo.py
    ├── coordenada.py
    └── rana.py
```

## Componentes Principales

### 1. Generador de Números Pseudoaleatorios

**Ubicación:** `generador_numeros/congruencia_lineal.py`

Implementa el método de **Congruencia Lineal** con la fórmula:

$$X_{n+1} = (a \cdot X_n + c) \bmod m$$

**Parámetros utilizados** (recomendados por Numerical Recipes):
- **a = 1664525** (multiplicador)
- **c = 1013904223** (incremento)
- **m = 2³²** (módulo)

Los números pseudoaleatorios uniformes en [0, 1) se obtienen mediante:

$$R_i = \frac{X_i}{m}$$

**Características:**
- Determinista: misma semilla = misma secuencia
- Período largo para asegurar buena cobertura estadística
- Parámetros optimizados para aplicaciones de simulación

### 2. Caminatas Aleatorias

#### Una Dimensión (`una_dimension/`)
En cada paso, la partícula se mueve hacia la izquierda o derecha con probabilidad 0.5:
- Si $R_i < 0.5$: movimiento izquierda (-1)
- Si $R_i \geq 0.5$: movimiento derecha (+1)

#### Dos Dimensiones (`dos_dimensiones/`)
En cada paso, la partícula se mueve en una de cuatro direcciones con probabilidad 0.25:
- $[0.00, 0.25)$: izquierda (-1, 0)
- $[0.25, 0.50)$: derecha (+1, 0)
- $[0.50, 0.75)$: arriba (0, +1)
- $[0.75, 1.00)$: abajo (0, -1)

#### Tres Dimensiones (`tres_dimensiones/`)
Extensión natural a seis direcciones posibles en el espacio 3D.

### 3. Validación de Números Pseudoaleatorios

**Ubicación:** `validacion_numeros/`

Se implementan tres pruebas estadísticas para validar la calidad de los números generados:

#### Uniformidad (`uniformidad.py`)
Verifica que los números pseudoaleatorios sigan una distribución uniforme en [0, 1).

#### Aleatoriedad (`aleatoriedad.py`)
Realiza pruebas para confirmar que los números son verdaderamente aleatorios.

#### No Correlación Serial (`no_correlacion_serial.py`)
Valida que no exista correlación entre números consecutivos en la secuencia.

## Requisitos

- Python 3.7+
- Librerías estándar de Python (sin dependencias externas obligatorias)
- Para visualizaciones opcionales: `matplotlib`, `numpy`

## Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd caminatas-aleatorias
```

### 2. Ejecutar una caminata aleatoria

**En una dimensión:**
```bash
python una_dimension/main.py
```

**En dos dimensiones:**
```bash
python dos_dimensiones/main.py
```

**En tres dimensiones:**
```bash
python tres_dimensiones/main.py
```

### 3. Validar la calidad de números pseudoaleatorios
```bash
python validacion_numeros/aleatoriedad.py
python validacion_numeros/uniformidad.py
python validacion_numeros/no_correlacion_serial.py
```

## Parámetros Configurables

Cada simulación incluye parámetros que se pueden modificar para ajustar el comportamiento:

### Parámetros Principales

| Parámetro | Descripción | Ubicación | Valor Predeterminado |
|-----------|-------------|-----------|----------------------|
| **numero_de_simulaciones** | Cantidad de caminatas aleatorias independientes a simular | Dentro de `main.py` | 100 |
| **pasos_por_simulacion** | Número de pasos en cada caminata aleatoria | Dentro de `main.py` | 1,000,000 |
| **paso_objetivo_para_probabilidad** | Paso específico para calcular la probabilidad de retorno al origen | Dentro de `main.py` | 1,000 |
| **semilla_base** | Semilla inicial para el generador de números pseudoaleatorios | Dentro de `main.py` | Auto-generada (basada en tiempo) |

### Cómo Modificar los Parámetros

Para cambiar los parámetros, edita el archivo `main.py` correspondiente a tu simulación. Por ejemplo, para una simulación en 1D:

**Archivo:** `una_dimension/main.py`

Busca la sección `if __name__ == "__main__":` al final del archivo:

```python
if __name__ == "__main__":
    # Modifica estos valores según necesites
    numero_de_simulaciones = 100              # Cambia número de simulaciones
    pasos_por_simulacion = 1000000           # Cambia número de pasos
    paso_objetivo_para_probabilidad = 1000   # Cambia paso objetivo
    
    # La semilla se genera automáticamente, pero puedes fijarla para reproducibilidad:
    # semilla_base = 12345  # Reemplaza con tu semilla
```

### Ejemplos de Configuración

#### Simulación Rápida (prueba)
```python
numero_de_simulaciones = 10
pasos_por_simulacion = 100
paso_objetivo_para_probabilidad = 50
```

#### Simulación Estándar (análisis moderado)
```python
numero_de_simulaciones = 100
pasos_por_simulacion = 10000
paso_objetivo_para_probabilidad = 1000
```

#### Simulación Intensiva (análisis detallado)
```python
numero_de_simulaciones = 1000
pasos_por_simulacion = 100000
paso_objetivo_para_probabilidad = 5000
```

### Descripción de Parámetros

**numero_de_simulaciones**
- Determina cuántas caminatas aleatorias independientes se ejecutarán
- Mayor número = mejores estadísticas pero más tiempo de ejecución
- Cada simulación usa una semilla diferente (semilla_base + i)

**pasos_por_simulacion**
- Número de pasos en cada caminata aleatoria
- Define la longitud de cada trayectoria
- Mayor número = análisis más detallado pero más tiempo de cálculo

**paso_objetivo_para_probabilidad**
- Paso específico para calcular la probabilidad de retorno al origen
- Debe ser menor que `pasos_por_simulacion`
- Se usa para analizar la probabilidad de estar en posición 0 después de N pasos

**semilla_base**
- Valor inicial para el generador de números pseudoaleatorios
- Si se fija: permite reproducir exactamente los mismos resultados
- Si se auto-genera: obtiene diferentes secuencias en cada ejecución

## Fundamentos Matemáticos

### Congruencia Lineal
El generador de congruencia lineal es uno de los más antiguos y utilizados. Produce números enteros mediante la recurrencia:

$$X_{n+1} = (a \cdot X_n + c) \bmod m$$

Para obtener uniformidad en [0, 1) se normaliza dividiendo entre $m$.

### Propiedades Deseables
- **Período máximo:** $p = m$ (alcanzado con parámetros correctos)
- **Distribución uniforme:** Los valores $R_i = X_i / m$ se distribuyen uniformemente
- **Determinismo:** Reproducibilidad con la misma semilla
- **Eficiencia:** Computacionalmente rápido

## Aplicaciones

Las caminatas aleatorias tienen aplicaciones en:
- **Física:** Movimiento browniano, difusión molecular
- **Finanzas:** Modelos de precios de activos (Movimiento Browniano Geométrico)
- **Biología:** Dispersión de organismos, búsqueda de alimento
- **Informática:** Algoritmos probabilísticos, Monte Carlo
- **Teoría de Grafos:** Exploración de redes

## Autor

Desarrollado como parte del taller de **Simulación de Computadores** - Semestre 9

---

**Nota:** Para obtener más detalles sobre la implementación específica, consulte los archivos de código y sus docstrings.
