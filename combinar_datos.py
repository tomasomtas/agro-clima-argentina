# combinar_datos.py
# Une datos climáticos con rendimientos agrícolas

import pandas as pd

print("🌱 COMBINANDO DATOS CLIMÁTICOS Y DE RENDIMIENTO")
print("=" * 60)

# 1. Cargar datos climáticos
print("📥 Cargando datos climáticos...")
clima = pd.read_csv("data/clima_argentina.csv", parse_dates=["date"])
clima["año"] = clima["date"].dt.year

# Resumir clima por provincia y año
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

print(f"✅ Clima resumido: {len(clima_resumen)} registros (10 provincias x 15 años)")

# 2. Cargar datos de rendimiento (generado por limpiar_csv.py)
print("📥 Cargando datos de rendimiento...")
try:
    rendimiento = pd.read_csv("data/rendimiento_argentina.csv")
    print(f"✅ Rendimiento cargado: {len(rendimiento)} registros (15 años)")
    print(f"📋 Cultivos disponibles: {rendimiento.columns.tolist()}")
except FileNotFoundError:
    print("❌ No se encontró 'data/rendimiento_argentina.csv'")
    print("   Ejecuta primero: python limpiar_csv.py")
    exit()

# 3. Unir datos
print("\n🔗 Combinando datos...")
master = clima_resumen.merge(rendimiento, on="año", how="inner")

# 4. Guardar dataset maestro
master.to_csv("data/master_dataset_final.csv", index=False, encoding="utf-8-sig")
print(f"\n✅ Dataset maestro guardado: {len(master)} registros x {len(master.columns)} columnas")

# 5. Mostrar vista previa
print("\n📊 Vista previa del dataset maestro:")
print(master.head())

# 6. Mostrar resumen por provincia
print("\n📊 Resumen por provincia (promedios 2010-2024):")
columnas_rendimiento = [col for col in master.columns if col.startswith("rend_")]
resumen_prov = master.groupby("provincia").agg({
    'temp_mean': 'mean',
    'precipitacion': 'mean',
    **{col: 'mean' for col in columnas_rendimiento[:4]}  # Primeros 4 cultivos
}).round(2)
print(resumen_prov)

print("\n🎉 ¡COMBINACIÓN COMPLETADA!")