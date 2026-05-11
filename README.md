# 🏗️ Relleno Hidráulico – Análisis Geomecánico  
Aplicación interactiva en **Streamlit** para evaluar parámetros geomecánicos, generar gráficos de presión vertical, comparar resultados de UCS a 28 días y producir un **reporte PDF profesional** mediante ReportLab.

---

## 🚀 Funcionalidades

### 📌 1. Análisis Geomecánico Completo
- Cálculo automático de:
  - Presiones verticales γ·z
  - Caso geométrico del caserón
  - Ángulo de falla α
  - Cohesión requerida *c*
  - Resistencia UCS\_RH (criterio Mitchell)

### 📌 2. Visualización de Resultados
- Gráfico de **Distribución de Presiones Verticales** (Plotly)
- Gráfico de **UCS a 28 días** con coloración por cumplimiento
- Indicadores con líneas de referencia para UCS requerida

### 📌 3. Generación de Reporte PDF
Produce un archivo PDF con:
- Datos del caserón y parámetros ingresados  
- Tablas completamente formateadas (estilo minero)  
- Gráficos incrustados (Plotly → PNG → ReportLab)  
- Encabezados, notas técnicas y fecha del análisis  
- Diseño profesional orientado a informes geotécnicos  

---

## 🛠️ Tecnología Utilizada

- **Python 3.10+**
- **Streamlit** – Interfaz web  
- **Plotly + Kaleido** – Generación de gráficos exportables  
- **ReportLab** – Construcción del PDF  
- **Pandas / NumPy** – Manejo de datos  
- **Matplotlib** (solo si aparece en código previo)  

---

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/usuario/proyecto-rh-geomecanico.git
cd proyecto-rh-geomecanico
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:

```bash
streamlit run app.py
```

---

## 🗂️ Estructura del Proyecto

```
📁 proyecto-rh-geomecanico
│── app.py
│── requirements.txt
│── README.md
└── assets/         # (opcional) logos e imágenes adicionales
```

---

## 📝 Notas Importantes

- Para evitar errores de exportación, **kaleido debe estar instalado**.
- En Streamlit Cloud, Kaleido funciona sin configuraciones adicionales.
- Si agregas nuevas secciones o pestañas, recuerda actualizar este README.

---

## 👤 Autor

**Bradoc Chambilla**  
Aplicación desarrollada para análisis de **Relleno Hidráulico (RH)** en minería subterránea.
