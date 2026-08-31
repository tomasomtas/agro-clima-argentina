# debug_cultivos.py
import pandas as pd
import re

print("🔍 DEPURANDO CULTIVOS")
print("=" * 60)

# Leer el archivo original
with open("data/production_argentina.csv", "r", encoding="utf-8-sig") as f:
    contenido = f.read()

lineas = contenido.strip().split("\n")
print(f"📄 Líneas totales: {len(lineas)}")

# Extraer cabecera
cabecera_raw = lineas[0]
match = re.search(r'"([^"]+)"', cabecera_raw)
if match:
    cabecera_limpia = match.group(1)
    columnas = [col.strip() for col in cabecera_limpia.split(",")]
else:
    columnas = ["CodigoAmbito", "Ambito", "CodigoArea", "Area", 
                "CodigoElemento", "Elemento", "CodigoProducto", "Producto",
                "CodigoAnio", "Anio", "Unidad", "Valor", 
                "Simbolo", "DescripcionSimbolo", "Nota"]

print(f"📋 Columnas: {columnas}")

# Procesar líneas de datos
datos = []
for linea in lineas[1:]:
    if not linea.strip():
        continue
    campos = re.findall(r'"([^"]*)"', linea)
    if not campos:
        campos = linea.strip().split(";")
    while len(campos) < len(columnas):
        campos.append("")
    if len(campos) > len(columnas):
        campos = campos[:len(columnas)]
    datos.append(campos)

df = pd.DataFrame(datos, columns=columnas)

# 1. Verificar Argentina
print(f"\n1. Registros de Argentina (código 32): {len(df[df['Area'] == '032'])}")

# 2. Ver todos los cultivos únicos
cultivos = df[df['Area'] == '032']['Producto'].unique().tolist()
print(f"\n2. Cultivos encontrados en Argentina: {len(cultivos)}")
print(f"   Primeros 20 cultivos:")
for i, c in enumerate(cultivos[:20], 1):
    print(f"   {i}. '{c}'")

# 3. Ver si hay Trigo, Maíz, Soja, etc.
cultivos_buscar = ['Trigo', 'Maíz', 'Soja', 'Girasol', 'Cebada', 'Sorgo']
print(f"\n3. Buscando cultivos principales:")
for c in cultivos_buscar:
    encontrados = [p for p in cultivos if c.lower() in p.lower()]
    if encontrados:
        print(f"   ✅ '{c}' encontrado como: {encontrados[:3]}")
    else:
        print(f"   ❌ '{c}' NO encontrado")

# 4. Ver elementos disponibles
elementos = df[df['Area'] == '032']['Elemento'].unique().tolist()
print(f"\n4. Elementos disponibles: {elementos}")