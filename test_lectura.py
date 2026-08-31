# test_lectura.py
import pandas as pd

# Intentar leer con diferentes configuraciones
print("📥 Probando lectura del archivo...")

try:
    # Opción 1: Usar punto y coma, y quotechar='"' para manejar comillas
    df = pd.read_csv(
        "data/production_argentina.csv",
        sep=';',
        encoding='utf-8-sig',
        quotechar='"',
        engine='python'  # Más tolerante que el engine 'c'
    )
    print(f"✅ Lectura exitosa! {len(df)} registros")
    print(f"📋 Columnas: {df.columns.tolist()}")
    print(f"\n📊 Primeras filas:")
    print(df.head())
    
except Exception as e:
    print(f"❌ Error: {e}")