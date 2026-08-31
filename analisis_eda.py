# analisis_eda.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv("data/master_dataset_final.csv")

print("📊 ANÁLISIS EXPLORATORIO DE DATOS")
print("=" * 60)

# 1. Información general
print(f"\n📋 Dataset: {df.shape[0]} filas, {df.shape[1]} columnas")
print(f"\n📋 Columnas: {df.columns.tolist()}")

# 2. Estadísticas descriptivas
print("\n📊 Estadísticas descriptivas:")
print(df.describe().round(2))

# 3. Correlación entre clima y rendimiento
print("\n🔍 Correlación entre variables climáticas y rendimiento:")
columnas_rendimiento = [col for col in df.columns if col.startswith("rend_")]
columnas_clima = ['temp_mean', 'precipitacion', 'horas_sol']

for cultivo in columnas_rendimiento[:3]:  # Primeros 3 cultivos
    print(f"\n   {cultivo}:")
    for clima_var in columnas_clima:
        corr = df[clima_var].corr(df[cultivo])
        print(f"      - {clima_var}: {corr:.3f}")

print("\n🎉 ¡Análisis completado!") 