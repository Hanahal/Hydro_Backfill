#  Relleno Hidráulico – Análisis Geomecánico y Granulométrico

Aplicación interactiva desarrollada en **Streamlit** para el análisis geomecánico y granulométrico aplicado a sistemas de **Relleno Hidráulico (RH)** en minería subterránea.

La plataforma permite evaluar parámetros geotécnicos, calcular resistencia UCS, analizar distribuciones granulométricas bajo normas ASTM, generar gráficos técnicos interactivos y producir un **reporte PDF profesional** mediante ReportLab.

---

#  Funcionalidades

##  1. Análisis Geomecánico Completo

Cálculo automático de:

- Presiones verticales γ·z
- Caso geométrico del caserón
- Ángulo de falla α
- Cohesión requerida *c*
- Resistencia UCS\_RH (criterio Mitchell)
- Evaluación de estabilidad del relleno hidráulico

---

##  2. Simulación y Evaluación UCS

Incluye:

- Comparación de resistencia UCS a 28 días
- Indicadores de cumplimiento geomecánico
- Líneas de referencia UCS requerida
- Visualización comparativa de resultados

---

##  3. Análisis Granulométrico ASTM

Módulo técnico para caracterización granulométrica del material de relleno.

### Normas Implementadas

- ASTM D6913 — Análisis granulométrico por tamices
- ASTM D2487 — Clasificación USCS
- ASTM D1140 — Determinación de finos pasante N°200

### Parámetros Calculados

- % retenido parcial
- % retenido acumulado
- % que pasa
- D10
- D30
- D60
- Coeficiente de uniformidad (Cu)
- Coeficiente de curvatura (Cc)
- Módulo de fineza
- Clasificación USCS

### Visualizaciones

- Curva granulométrica semilogarítmica
- Distribución grava–arena–finos
- Barras de retenido parcial
- Verificación ASTM automática

---

##  4. Visualización de Resultados

### Gráficos Interactivos

- Distribución de Presiones Verticales (Plotly)
- UCS a 28 días con validación visual
- Curvas granulométricas ASTM
- Distribución por fracciones granulométricas
- Indicadores técnicos geomecánicos

---

##  5. Generación de Reporte PDF

Produce automáticamente un reporte técnico profesional con:

- Datos del caserón
- Parámetros geomecánicos
- Resultados UCS
- Tablas granulométricas ASTM
- Clasificación USCS
- Gráficos incrustados
- Notas técnicas y observaciones
- Fecha del análisis

### Características del PDF

- Diseño orientado a ingeniería minera
- Tablas técnicas formateadas
- Diagramas incrustados
- Exportación profesional automática

---

#  Tecnología Utilizada

- **Python 3.10+**
- **Streamlit** — Interfaz web interactiva
- **Plotly + Kaleido** — Gráficos exportables
- **ReportLab** — Construcción del PDF
- **Pandas / NumPy** — Manejo de datos
- **SciPy** — Cálculos estadísticos y granulométricos
- **Matplotlib** — Visualizaciones complementarias

---

#  Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/proyecto-rh-geomecanico.git
cd proyecto-rh-geomecanico
