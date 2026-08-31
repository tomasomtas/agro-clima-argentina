# dashboard.py
# Dashboard interactivo de clima y rendimiento agrícola en Argentina

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="AgroClima Argentina",
    page_icon="🌾",
    layout="wide"
)

# Título
st.title("🌾 AgroClima Argentina")
st.markdown("""
**Análisis interactivo de la relación entre clima y rendimiento agrícola**  
Explora cómo las variables climáticas afectan la producción de los principales cultivos argentinos.
""")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/master_dataset_final.csv")
    return df

df = load_data()

# Sidebar - Filtros
st.sidebar.header("🔧 Filtros")

# Selección de provincia
provincias = sorted(df['provincia'].unique())
provincia_seleccionada = st.sidebar.selectbox(
    "Seleccionar provincia",
    options=["Todas"] + provincias
)

# Rango de años
years = sorted(df['año'].unique())
year_range = st.sidebar.slider(
    "Rango de años",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years)))
)

# Selección de cultivo
cultivos = [col for col in df.columns if col.startswith("rend_")]
cultivos_nombres = {
    "rend_Cebada": "Cebada",
    "rend_Grano se soja": "Soja",
    "rend_Maíz": "Maíz",
    "rend_Semilla de girasol": "Girasol",
    "rend_Sorgo": "Sorgo",
    "rend_Trigo": "Trigo"
}
cultivo_seleccionado = st.sidebar.selectbox(
    "Seleccionar cultivo",
    options=cultivos,
    format_func=lambda x: cultivos_nombres.get(x, x)
)

# Variable climática
variables_clima = ['temp_mean', 'temp_max', 'temp_min', 'precipitacion', 'horas_sol']
variables_nombres = {
    'temp_mean': 'Temperatura media (°C)',
    'temp_max': 'Temperatura máxima (°C)',
    'temp_min': 'Temperatura mínima (°C)',
    'precipitacion': 'Precipitación (mm)',
    'horas_sol': 'Horas de sol'
}
var_clima = st.sidebar.selectbox(
    "Variable climática",
    options=variables_clima,
    format_func=lambda x: variables_nombres.get(x, x)
)

# Aplicar filtros
df_filtrado = df[
    (df['año'] >= year_range[0]) &
    (df['año'] <= year_range[1])
]

if provincia_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['provincia'] == provincia_seleccionada]

# --- MÉTRICAS ---
st.subheader("📊 Indicadores clave")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_temp = df_filtrado['temp_mean'].mean()
    st.metric("Temperatura media", f"{avg_temp:.1f}°C")

with col2:
    avg_precip = df_filtrado['precipitacion'].mean()
    st.metric("Precipitación promedio", f"{avg_precip:.0f} mm")

with col3:
    avg_yield = df_filtrado[cultivo_seleccionado].mean()
    st.metric(f"Rendimiento promedio ({cultivos_nombres[cultivo_seleccionado]})", f"{avg_yield:,.0f} t")

with col4:
    prov_count = df_filtrado['provincia'].nunique()
    st.metric("Provincias analizadas", prov_count)

# --- GRÁFICOS ---
st.subheader("📈 Evolución temporal")

col1, col2 = st.columns(2)

with col1:
    # Evolución del rendimiento
    fig_yield = px.line(
        df_filtrado,
        x='año',
        y=cultivo_seleccionado,
        color='provincia' if provincia_seleccionada == "Todas" else None,
        title=f'Evolución del rendimiento de {cultivos_nombres[cultivo_seleccionado]}',
        labels={cultivo_seleccionado: 'Rendimiento (t)', 'año': 'Año', 'provincia': 'Provincia'}
    )
    st.plotly_chart(fig_yield, use_container_width=True)

with col2:
    # Relación clima vs rendimiento
    fig_scatter = px.scatter(
        df_filtrado,
        x=var_clima,
        y=cultivo_seleccionado,
        color='provincia' if provincia_seleccionada == "Todas" else None,
        size='año',
        hover_name='provincia',
        title=f'Relación: {variables_nombres[var_clima]} vs Rendimiento',
        labels={
            var_clima: variables_nombres[var_clima],
            cultivo_seleccionado: f'Rendimiento {cultivos_nombres[cultivo_seleccionado]} (t)'
        }
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- MAPA DE CALOR (CORRELACIONES) ---
st.subheader("🔍 Correlaciones entre clima y rendimiento")

# Calcular correlaciones por provincia
corr_data = []
for prov in df['provincia'].unique():
    df_prov = df[df['provincia'] == prov]
    for cultivo in cultivos:
        for var in variables_clima:
            corr = df_prov[var].corr(df_prov[cultivo])
            if not pd.isna(corr):
                corr_data.append({
                    'provincia': prov,
                    'cultivo': cultivos_nombres.get(cultivo, cultivo),
                    'variable': variables_nombres.get(var, var),
                    'correlacion': corr
                })

df_corr = pd.DataFrame(corr_data)

# Filtro de cultivo para el mapa de calor
cultivo_corr = st.selectbox(
    "Cultivo para mapa de correlaciones",
    options=cultivos,
    format_func=lambda x: cultivos_nombres.get(x, x)
)

df_corr_filt = df_corr[df_corr['cultivo'] == cultivos_nombres.get(cultivo_corr, cultivo_corr)]

fig_corr = px.bar(
    df_corr_filt,
    x='provincia',
    y='correlacion',
    color='variable',
    barmode='group',
    title=f'Correlaciones por provincia - {cultivos_nombres[cultivo_corr]}',
    labels={'correlacion': 'Correlación', 'provincia': 'Provincia', 'variable': 'Variable climática'}
)
st.plotly_chart(fig_corr, use_container_width=True)

# --- TABLA DE DATOS ---
with st.expander("📋 Ver datos completos"):
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Descargar
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar datos filtrados (CSV)",
        data=csv,
        file_name="datos_filtrados.csv",
        mime="text/csv"
    )

st.divider()
st.caption("🌾 AgroClima Argentina | Datos: FAOSTAT + Open-Meteo | Hecho con Streamlit")