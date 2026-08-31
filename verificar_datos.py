# verificar_datos.py
import pandas as pd

# Cargar los datos
df = pd.read_csv("data/clima_argentina.csv", parse_dates=["date"])

print("📊 RESUMEN DE DATOS CLIMÁTICOS")
print("=" * 40)
print(f"Registros totales: {len(df):,}")
print(f"Provincias: {df['provincia'].nunique()}")
print(f"Rango de fechas: {df['date'].min()} a {df['date'].max()}")
print(f"\nColumnas: {df.columns.tolist()}")

print("\n📋 MUESTRA DE DATOS")
print("=" * 40)
print(df.head(10))

print("\n📊 RESUMEN POR PROVINCIA")
print("=" * 40)
resumen = df.groupby('provincia').agg({
    'temp_mean': 'mean',
    'precipitacion': 'sum',
    'temp_max': 'mean',
    'temp_min': 'mean'
}).round(2)

print(resumen)