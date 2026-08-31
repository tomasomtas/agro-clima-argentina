markdown
# 🌾 AgroClima Argentina

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tu-usuario-agro-clima-argentina.streamlit.app/)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📊 Descripción del Proyecto

**AgroClima Argentina** es un dashboard interactivo diseñado para analizar la relación entre las variables climáticas y el rendimiento de los principales cultivos agrícolas en Argentina. 

El proyecto combina datos climáticos históricos de **Open-Meteo** (temperaturas, precipitación, horas de sol, viento, evapotranspiración) con datos de rendimiento agrícola por provincia del **Ministerio de Agricultura de Argentina**, permitiendo explorar cómo el clima afecta la producción de cultivos como Trigo, Maíz, Soja, Girasol, Cebada y Sorgo.

---

## 🎯 ¿Qué permite analizar?

El dashboard permite responder preguntas como:

- **¿Cómo ha evolucionado el rendimiento de la soja en Buenos Aires en la última década?**
- **¿Qué provincias tienen el mejor rendimiento de maíz?**
- **¿Existe relación entre la precipitación y el rendimiento del trigo?**
- **¿Cómo se correlacionan las variables climáticas con el rendimiento de cada cultivo?**
- **¿Qué provincias son más productivas para cada cultivo?**

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| **Python** | Lenguaje principal de programación |
| **Streamlit** | Framework para crear el dashboard interactivo |
| **Pandas** | Procesamiento y manipulación de datos |
| **Plotly** | Generación de gráficos interactivos |
| **Folium** | Mapas detallados de Argentina |
| **Open-Meteo API** | Fuente de datos climáticos históricos |
| **Estimaciones Agrícolas (Argentina)** | Datos de rendimiento por provincia |

---

## 📁 Fuentes de datos

### Datos climáticos
- **Open-Meteo API**: Datos históricos (2010-2024) de temperatura, precipitación, horas de sol, viento y evapotranspiración para 10 provincias argentinas.

### Datos de rendimiento agrícola
- **Ministerio de Agricultura de Argentina (Estimaciones Agrícolas)**: Rendimiento (kg/ha) por provincia y campaña para los principales cultivos argentinos.

---

## 📋 Funcionalidades del dashboard

### 🔧 Filtros interactivos
- **Provincia**: selecciona una provincia o "Todas"
- **Años**: rango de años a analizar
- **Cultivo**: elige entre Cebada, Girasol, Maíz, Soja, Sorgo o Trigo
- **Variable climática**: temperatura media, máxima, mínima, precipitación u horas de sol

### 📊 Visualizaciones
- **Métricas clave**: temperatura media, precipitación, rendimiento promedio y provincias analizadas
- **Evolución temporal**: gráfico de líneas del rendimiento a lo largo del tiempo
- **Relación clima vs rendimiento**: gráfico de dispersión interactivo
- **Correlaciones por provincia**: barras que muestran la correlación entre cada variable climática y el rendimiento
- **Mapa de Argentina**: círculos de colores según el rendimiento por provincia
- **Mapa detallado con Folium**: marcadores interactivos con información de cada provincia

### 💾 Exportación
- Descarga de datos filtrados en formato CSV

---

## 🚀 Cómo ejecutar el proyecto

### Requisitos previos
- Python 3.10 o superior
- Git (opcional)

### Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/agro-clima-argentina.git
cd agro-clima-argentina

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el dashboard
streamlit run dashboard_provincial.py
Dependencias (requirements.txt)
txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.18.0
numpy>=1.24.0
folium>=0.14.0
streamlit-folium>=0.15.0
📂 Estructura del proyecto
text
agro-clima-argentina/
├── dashboard_provincial.py          # Dashboard principal
├── integrar_rendimiento_provincial.py # Script para integrar datos
├── requirements.txt                 # Dependencias del proyecto
├── data/
│   ├── clima_argentina.csv          # Datos climáticos (Open-Meteo)
│   └── master_dataset_provincial.csv # Dataset final combinado
├── README.md                        # Documentación del proyecto
└── .gitignore
🔍 Metodología
Obtención de datos climáticos: Descarga automática desde Open-Meteo API para 10 provincias argentinas (2010-2024).

Obtención de datos agrícolas: Extracción de rendimientos por provincia desde las estimaciones del Ministerio de Agricultura.

Integración: Combinación de ambos datasets por provincia y año.

Análisis: Cálculo de correlaciones entre variables climáticas y rendimientos.

Visualización: Dashboard interactivo para explorar los datos.

📈 Resultados clave (ejemplos)
Correlaciones: Se observa que la precipitación tiene una correlación positiva con el rendimiento de soja en varias provincias, mientras que la temperatura media muestra correlaciones mixtas según el cultivo y la región.

Variabilidad provincial: Buenos Aires y Córdoba lideran los rendimientos de la mayoría de los cultivos, mientras que provincias del norte (Salta, Santiago del Estero) muestran patrones climáticos y productivos diferentes.

🔮 Mejoras futuras
□ Agregar pronósticos climáticos para estimar rendimiento futuro
□ Incorporar datos de superficie sembrada y producción total
□ Incluir análisis de series temporales con modelos ARIMA
□ Crear modelos predictivos con Machine Learning (XGBoost)
□ Agregar datos de precios de commodities
□ Desplegar en Streamlit Cloud para acceso público
🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerir mejoras.

📝 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más información.

📬 Contacto
Si tienes preguntas, sugerencias o quieres colaborar, no dudes en contactarme.

GitHub: https://github.com/tomasomtas

LinkedIn: https://www.linkedin.com/in/diego-tomas-beorlegui/

Email: dbeorlegui@agro.uba.ar

¡Gracias por visitar el proyecto! 🌾🇦🇷