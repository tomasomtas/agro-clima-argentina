# integrar_rendimiento_provincial.py
import pandas as pd
import re

print("🌱 INTEGRANDO RENDIMIENTO PROVINCIAL CON CLIMA")
print("=" * 70)

# 1. Cargar datos climáticos
print("\n📥 Cargando datos climáticos...")
clima = pd.read_csv("data/clima_argentina.csv", parse_dates=["date"])
clima["año"] = clima["date"].dt.year

clima_resumen = clima.groupby(["provincia", "año"]).agg({
    'temp_mean': 'mean',
    'temp_max': 'mean',
    'temp_min': 'mean',
    'precipitacion': 'sum',
    'lluvia': 'sum',
    'horas_sol': 'sum',
    'viento_max': 'mean',
    'evapotranspiracion': 'sum'
}).reset_index()

# Normalizar nombres de provincias en clima
def normalizar_provincia_clima(nombre):
    return nombre.replace('_', ' ').upper()

clima_resumen["provincia_norm"] = clima_resumen["provincia"].apply(normalizar_provincia_clima)
print(f"✅ Clima resumido: {len(clima_resumen)} registros")

# 2. Cargar el archivo de estimaciones
print("\n📥 Cargando estimaciones agrícolas...")

# Lista de encodings para probar
encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8-sig']
df = None
for enc in encodings:
    try:
        df = pd.read_csv("data/Estimaciones.csv", sep=";", encoding=enc)
        print(f"✅ Archivo cargado con encoding: {enc}")
        print(f"   Registros: {len(df)}")
        break
    except Exception as e:
        print(f"   ❌ Falló con encoding {enc}: {str(e)[:50]}")
        continue

if df is None:
    print("❌ No se pudo cargar el archivo con ningún encoding")
    exit()

# 3. Limpiar nombres de columnas y eliminar acentos/ñ
df.columns = df.columns.str.strip()

# Renombrar columnas para evitar problemas con ñ
df.columns = ['Cultivo', 'Campana', 'Provincia', 'idProvincia', 'Sup_Sembrada', 'Produccion', 'Rendimiento']
print(f"📋 Columnas renombradas: {df.columns.tolist()}")

# 4. Extraer año de la campaña
def extraer_anio(campana):
    if pd.isna(campana):
        return None
    campana = str(campana).strip()
    match = re.search(r'(\d{4})', campana)
    if match:
        return int(match.group(1))
    return None

df["año"] = df["Campana"].apply(extraer_anio)
print(f"✅ Años extraídos: {df['año'].min()} - {df['año'].max()}")

# 5. Filtrar cultivos principales
cultivos_principales = ["Trigo", "Maíz", "Soja", "Girasol", "Cebada", "Sorgo"]
patron = "|".join(cultivos_principales)
df_filtrado = df[df["Cultivo"].str.contains(patron, case=False, na=False)].copy()
print(f"✅ Cultivos filtrados: {df_filtrado['Cultivo'].unique().tolist()}")

# 6. Normalizar nombres de cultivos
def normalizar_cultivo(nombre):
    nombre = str(nombre).lower()
    if "trigo" in nombre:
        return "Trigo"
    elif "soja" in nombre:
        return "Soja"
    elif "maíz" in nombre or "maiz" in nombre:
        return "Maíz"
    elif "girasol" in nombre:
        return "Girasol"
    elif "cebada" in nombre:
        return "Cebada"
    elif "sorgo" in nombre:
        return "Sorgo"
    return nombre

df_filtrado["Cultivo_normalizado"] = df_filtrado["Cultivo"].apply(normalizar_cultivo)
print(f"✅ Cultivos normalizados: {df_filtrado['Cultivo_normalizado'].unique().tolist()}")

# 7. Agrupar por provincia, año y cultivo
df_agrupado = df_filtrado.groupby(["Provincia", "año", "Cultivo_normalizado"]).agg({
    "Sup_Sembrada": "sum",
    "Produccion": "sum",
    "Rendimiento": "mean"
}).reset_index()

# 8. Pivotear rendimiento
rendimiento_pivot = df_agrupado.pivot_table(
    index=["Provincia", "año"],
    columns="Cultivo_normalizado",
    values="Rendimiento"
).reset_index()

# Renombrar columnas
rendimiento_pivot.columns = ["provincia_est", "año"] + [f"rend_{c}" for c in rendimiento_pivot.columns[2:]]

print(f"✅ Rendimiento pivotado: {rendimiento_pivot.shape}")

# 9. Unir con clima usando provincia_norm
print("\n🔗 Combinando datos...")
master = clima_resumen.merge(
    rendimiento_pivot,
    left_on=["provincia_norm", "año"],
    right_on=["provincia_est", "año"],
    how="inner"
)

# 10. Guardar
master.to_csv("data/master_dataset_provincial.csv", index=False, encoding="utf-8-sig")
print(f"\n✅ Dataset provincial guardado: {len(master)} registros x {len(master.columns)} columnas")

# 11. Mostrar vista previa
if len(master) > 0:
    print("\n📊 Vista previa:")
    print(master.head())
    
    print("\n📊 Resumen por provincia (promedios 2010-2024):")
    columnas_rend = [col for col in master.columns if col.startswith("rend_")]
    if columnas_rend:
        resumen = master.groupby("provincia")[["temp_mean", "precipitacion"] + columnas_rend[:3]].mean().round(2)
        print(resumen)
else:
    print("\n⚠️ El dataset está vacío. Verificando nombres de provincias...")
    print("\n🔍 Provincias en clima (normalizadas):")
    print(clima_resumen["provincia_norm"].unique().tolist())
    print("\n🔍 Provincias en estimaciones:")
    print(rendimiento_pivot["provincia_est"].unique().tolist())

print("\n🎉 ¡INTEGRACIÓN COMPLETADA!")