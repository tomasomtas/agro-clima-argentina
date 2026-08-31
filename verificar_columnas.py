# verificar_columnas.py
import pandas as pd

# Cargar el archivo
df = pd.read_csv("data/production_argentina.csv", sep=';', encoding='utf-8-sig')

# Mostrar columnas
print("📋 Columnas del archivo:")
print(df.columns.tolist())

# Mostrar primeras filas
print("\n📊 Primeras filas:")
print(df.head())