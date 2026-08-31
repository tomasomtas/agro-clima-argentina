# dashboard_provincial.py
# Dashboard interactivo con datos climáticos y rendimiento por provincia

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Coordenadas de provincias argentinas (centro aproximado)
coordenadas_provincias = {
    "Buenos_Aires": {"lat": -36.0, "lon": -60.0},
    "Cordoba": {"lat": -32.0, "lon": -64.0},
    "Santa_Fe": {"lat": -31.0, "lon": -61.0},
    "Entre_Rios": {"lat": -32.0, "lon": -59.0},
    "Salta": {"lat": -24.5, "lon": -64.0},
    "Santiago_del_Estero": {"lat": -28.0, "lon": -63.0},
    "Chaco": {"lat": -27.0, "lon": -59.0},
    "La_Pampa": {"lat": -37.0, "lon": -65.0},
    "Tucuman": {"lat": -27.0, "lon": -65.5},
    "Mendoza": {"lat": -33.0, "lon": -68.0},
    "Corrientes": {"lat": -29.0, "lon": -58.0},
    "Formosa": {"lat": -26.0, "lon": -58.0},
    "Misiones": {"lat": -27.0, "lon": -55.0},
    "San_Luis": {"lat": -33.0, "lon": -66.0},
    "Catamarca": {"lat": -28.5, "lon": -66.0},
    "Jujuy": {"lat": -24.0, "lon": -65.0},
    "La_Rioja": {"lat": -29.0, "lon": -67.0},
    "Rio_Negro": {"lat": -39.0, "lon": -67.0},
    "Neuquen": {"lat": -39.0, "lon": -69.0},
    "Chubut": {"lat": -43.0, "lon": -68.0},
    "Santa_Cruz": {"lat": -49.0, "lon": -69.0},
    "Tierra_del_Fuego": {"lat": -54.0, "lon": -68.0}
}

# Configuración de la página
st.set_page_config(
    page_title="AgroClima Argentina - Provincial",
    page_icon="🌾",
    layout="wide"
)

# Título
st.title("🌾 AgroClima Argentina")
st.markdown("""
**Análisis interactivo de la relación entre clima y rendimiento agrícola por provincia**  
Explora cómo las variables climáticas afectan la producción de los principales cultivos argentinos.
""")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/master_dataset_provincial.csv")
    return df

df = load_data()

# ---- SIDEBAR - FILTROS ----
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
    "rend_Girasol": "Girasol",
    "rend_Maíz": "Maíz",
    "rend_Soja": "Soja",
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

# ---- MÉTRICAS ----
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
    st.metric(f"Rendimiento ({cultivos_nombres[cultivo_seleccionado]})", f"{avg_yield:,.0f} kg/ha")

with col4:
    prov_count = df_filtrado['provincia'].nunique()
    st.metric("Provincias analizadas", prov_count)

# ---- GRÁFICOS ----
st.subheader("📈 Análisis temporal")

col1, col2 = st.columns(2)

with col1:
    # Evolución del rendimiento por provincia
    fig_yield = px.line(
        df_filtrado,
        x='año',
        y=cultivo_seleccionado,
        color='provincia' if provincia_seleccionada == "Todas" else None,
        title=f'Evolución del rendimiento de {cultivos_nombres[cultivo_seleccionado]}',
        labels={
            cultivo_seleccionado: 'Rendimiento (kg/ha)',
            'año': 'Año',
            'provincia': 'Provincia'
        }
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
            cultivo_seleccionado: f'Rendimiento (kg/ha)'
        }
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ---- MAPA DE CORRELACIONES ----
st.subheader("🔍 Correlaciones entre clima y rendimiento por provincia")

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
    "Cultivo para análisis de correlaciones",
    options=cultivos,
    format_func=lambda x: cultivos_nombres.get(x, x)
)

df_corr_filt = df_corr[df_corr['cultivo'] == cultivos_nombres.get(cultivo_corr, cultivo_corr)]

if not df_corr_filt.empty:
    fig_corr = px.bar(
        df_corr_filt,
        x='provincia',
        y='correlacion',
        color='variable',
        barmode='group',
        title=f'Correlaciones por provincia - {cultivos_nombres[cultivo_corr]}',
        labels={
            'correlacion': 'Correlación',
            'provincia': 'Provincia',
            'variable': 'Variable climática'
        }
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("No hay datos suficientes para mostrar correlaciones")

# ---- MAPA DE ARGENTINA (Rendimiento por provincia) ----
st.subheader("🗺️ Mapa de rendimiento por provincia")

# Datos para el mapa (promedio por provincia para el cultivo seleccionado)
df_mapa = df.groupby('provincia')[cultivo_seleccionado].mean().reset_index()
df_mapa.columns = ['provincia', 'rendimiento']

# Agregar coordenadas
df_mapa['lat'] = df_mapa['provincia'].map(lambda x: coordenadas_provincias.get(x, {}).get('lat'))
df_mapa['lon'] = df_mapa['provincia'].map(lambda x: coordenadas_provincias.get(x, {}).get('lon'))

# ELIMINAR FILAS CON VALORES NULOS (evita el error de NaN en 'size')
df_mapa = df_mapa.dropna(subset=['rendimiento', 'lat', 'lon'])

if not df_mapa.empty:
    # Usar scatter_geo (más estable, no requiere Mapbox)
    fig_mapa = px.scatter_geo(
        df_mapa,
        lat="lat",
        lon="lon",
        size="rendimiento",
        color="rendimiento",
        hover_name="provincia",
        hover_data={"rendimiento": ":,.0f kg/ha"},
        title=f'Rendimiento promedio de {cultivos_nombres[cultivo_seleccionado]} por provincia (2010-2024)',
        color_continuous_scale="Viridis",
        size_max=30,
        projection="natural earth"
    )
    
    # Ajustar el foco en Argentina
    fig_mapa.update_geos(
        center=dict(lat=-36.0, lon=-63.0),
        lonaxis_range=[-75, -55],
        lataxis_range=[-55, -20],
        showcountries=True,
        countrycolor="Black",
        showsubunits=True,
        subunitcolor="Blue"
    )
    
    fig_mapa.update_layout(height=500)
    st.plotly_chart(fig_mapa, use_container_width=True)
else:
    st.info("No hay datos suficientes para mostrar el mapa")

# ---- MAPA CON FOLIUM (alternativo) ----
st.subheader("🗺️ Mapa detallado de Argentina")

# Verificar que hay datos para el mapa
if not df_mapa.empty:
    try:
        import folium
        from streamlit_folium import st_folium
        
        # Coordenadas para centrar en Argentina
        m = folium.Map(location=[-36.0, -63.0], zoom_start=5, tiles='OpenStreetMap')
        
        # Agregar marcadores por provincia
        for _, row in df_mapa.iterrows():
            # Calcular radio (mínimo 5, máximo 30)
            radius = max(5, min(30, row['rendimiento'] / 1500))
            
            popup_text = f"""
            <b>{row['provincia']}</b><br>
            Rendimiento: {row['rendimiento']:,.0f} kg/ha
            """
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=radius,
                popup=popup_text,
                color='green',
                fill=True,
                fillColor='darkgreen',
                fillOpacity=0.6
            ).add_to(m)
        
        # Mostrar el mapa
        st_folium(m, width=700, height=500)
    except ImportError:
        st.warning("⚠️ Para ver el mapa detallado, instala: `pip install folium streamlit-folium`")
else:
    st.info("No hay datos suficientes para mostrar el mapa detallado")

# ---- TABLA DE DATOS ----
with st.expander("📋 Ver datos completos"):
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Descargar
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar datos filtrados (CSV)",
        data=csv,
        file_name="datos_filtrados_provincial.csv",
        mime="text/csv"
    )

st.divider()
st.caption("🌾 AgroClima Argentina | Datos: FAOSTAT + Estimaciones Agrícolas + Open-Meteo | Hecho con Streamlit")