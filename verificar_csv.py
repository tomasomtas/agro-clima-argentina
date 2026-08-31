# verificar_csv.py
import pandas as pd

# Probar diferentes separadores
print("Probando separador ',' (coma)...")
try:
    df = pd.read_csv("data/production_argentina.csv", sep=',', encoding='utf-8-sig')
    print(f"✅ Funciona! Columnas: {df.columns.tolist()}")
    print(df.head())
except Exception as e:
    print(f"❌ Error: {e}")