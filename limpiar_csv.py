# limpiar_csv.py
import pandas as pd
import re

print("🧹 LIMPIANDO ARCHIVO PRODUCCIÓN ARGENTINA (VERSIÓN FINAL)")
print("=" * 70)

# Leer el archivo línea por línea
with open("data/production_argentina.csv", "r", encoding="utf-8-sig") as f:
    contenido = f.read()

# Dividir en líneas
lineas = contenido.strip().split("\n")
print(f"📄 Líneas totales: {len(lineas)}")

# --- PROCESAR CADA LÍNEA DE FORMA MANUAL ---
datos = []
for i, linea in enumerate(lineas):
    if i == 0:  # Saltar cabecera
        continue
    
    if not linea.strip():
        continue
    
    # Limpiar la línea: eliminar caracteres extraños
    linea_limpia = linea.strip()
    
    # Extraer campos entre comillas dobles
    campos = re.findall(r'"([^"]*)"', linea_limpia)
    
    # Si hay exactamente 15 campos, es el formato esperado
    if len(campos) == 15:
        datos.append(campos)
    else:
        # Si no, intentar dividir por punto y coma
        campos = linea_limpia.split(";")
        # Limpiar cada campo (quitar comillas)
        campos = [c.strip().strip('"') for c in campos]
        if len(campos) == 15:
            datos.append(campos)
        else:
            # Si aún no, intentar dividir por coma
            campos = linea_limpia.split(",")
            campos = [c.strip().strip('"') for c in campos]
            if len(campos) == 15:
                datos.append(campos)
    
    if (i + 1) % 500 == 0:
        print(f"   Procesando línea {i+1}...")

print(f"✅ Datos extraídos: {len(datos)} registros")

# Verificar que tenemos datos
if len(datos) == 0:
    print("❌ No se extrajeron datos. Verifica el formato del archivo.")
    exit()

# Crear DataFrame
columnas = [
    "CodigoAmbito", "Ambito", "CodigoArea", "Area",
    "CodigoElemento", "Elemento", "CodigoProducto", "Producto",
    "CodigoAnio", "Anio", "Unidad", "Valor",
    "Simbolo", "DescripcionSimbolo", "Nota"
]

df = pd.DataFrame(datos, columns=columnas)

# Mostrar información del DataFrame
print(f"\n📊 DataFrame creado: {len(df)} filas, {len(df.columns)} columnas")
print(f"📋 Columnas: {df.columns.tolist()}")

# Verificar valores únicos en Elemento
print(f"\n🔍 Elementos encontrados: {df['Elemento'].unique().tolist()}")
print(f"🔍 Áreas encontradas: {df['Area'].unique().tolist()[:10]}")

# --- CORRECCIÓN: Filtrar Argentina por nombre, no por código ---
df_arg = df[df["Area"] == "Argentina"].copy()
print(f"\n✅ Argentina (por nombre): {len(df_arg)} registros")

if len(df_arg) == 0:
    print("⚠️ No se encontraron datos para Argentina")
    print(f"   Áreas disponibles: {df['Area'].unique().tolist()[:20]}")
    exit()

# Limpiar valores numéricos
def limpiar_numero(val):
    if pd.isna(val) or val == "":
        return None
    val = str(val).replace(",", "").replace(" ", "").strip()
    if val == "":
        return None
    try:
        return float(val)
    except:
        return None

# Aplicar limpieza a la columna Valor
df_arg["Valor_limpio"] = df_arg["Valor"].apply(limpiar_numero)

# Verificar elementos en Argentina
print(f"🔍 Elementos en Argentina: {df_arg['Elemento'].unique().tolist()}")

# Pivotear para tener los 3 indicadores como columnas
df_pivot = df_arg.pivot_table(
    index=["Producto", "Anio"],
    columns="Elemento",
    values="Valor_limpio"
).reset_index()

# Renombrar columnas
df_pivot.columns = ["Producto", "Anio", "Area_cosechada", "Produccion", "Rendimiento"]

print(f"\n✅ Datos pivotados: {len(df_pivot)} registros")
print(f"📋 Columnas: {df_pivot.columns.tolist()}")

# Guardar datos completos
df_pivot.to_csv("data/production_clean_complete.csv", index=False, encoding="utf-8-sig")
print("\n✅ Archivo guardado: data/production_clean_complete.csv")

# ---- FILTRAR CULTIVOS PRINCIPALES ----
# Buscar cultivos que coincidan con los patrones
patrones_cultivos = {
    "Trigo": "trigo",
    "Maíz": ["maíz", "maiz", "corn"],
    "Soja": ["soja", "soya", "soybean"],
    "Girasol": ["girasol", "sunflower"],
    "Cebada": ["cebada", "barley"],
    "Sorgo": ["sorgo", "sorghum"]
}

cultivos_seleccionados = []
for nombre, patron in patrones_cultivos.items():
    if isinstance(patron, list):
        for p in patron:
            encontrados = [c for c in df_pivot["Producto"].unique() if p.lower() in str(c).lower()]
            if encontrados:
                cultivos_seleccionados.extend(encontrados)
                print(f"   ✅ '{nombre}' encontrado como: {encontrados[0]}")
                break
    else:
        encontrados = [c for c in df_pivot["Producto"].unique() if patron.lower() in str(c).lower()]
        if encontrados:
            cultivos_seleccionados.extend(encontrados)
            print(f"   ✅ '{nombre}' encontrado como: {encontrados[0]}")

# Si no se encontraron todos, mostrar los disponibles
if not cultivos_seleccionados or len(cultivos_seleccionados) < 6:
    print("\n⚠️ Algunos cultivos no se encontraron. Mostrando todos los cultivos disponibles:")
    cultivos = df_pivot["Producto"].unique().tolist()
    for i, c in enumerate(cultivos[:20], 1):
        print(f"   {i}. '{c}'")
    
    # Tomar los primeros 6 cultivos como fallback
    if not cultivos_seleccionados:
        cultivos_seleccionados = cultivos[:6]
        print(f"\n⚠️ Usando primeros 6 cultivos como fallback: {cultivos_seleccionados}")

# Eliminar duplicados
cultivos_seleccionados = list(set(cultivos_seleccionados))
print(f"\n✅ Cultivos seleccionados: {cultivos_seleccionados}")

# Filtrar
df_rendimiento = df_pivot[df_pivot["Producto"].isin(cultivos_seleccionados)].copy()

if len(df_rendimiento) == 0:
    print("❌ No se encontraron datos para los cultivos seleccionados")
    exit()

print(f"✅ Registros de rendimiento: {len(df_rendimiento)}")

# Pivotear por cultivo para rendimiento
df_rendimiento_pivot = df_rendimiento.pivot_table(
    index="Anio",
    columns="Producto",
    values="Rendimiento"
).reset_index()

# Renombrar columnas
nombres_columnas = ["año"] + [f"rend_{c}" for c in df_rendimiento_pivot.columns[1:]]
df_rendimiento_pivot.columns = nombres_columnas

# Guardar
df_rendimiento_pivot.to_csv("data/rendimiento_argentina.csv", index=False, encoding="utf-8-sig")
print("\n✅ Archivo de rendimiento guardado: data/rendimiento_argentina.csv")

# Mostrar vista previa
print("\n📊 Vista previa (rendimiento):")
print(df_rendimiento_pivot.head())

# Mostrar resumen
if not df_rendimiento.empty:
    print("\n📊 Resumen de rendimiento por cultivo (promedio 2010-2024):")
    resumen = df_rendimiento.groupby("Producto")["Rendimiento"].mean().round(2)
    print(resumen)

print("\n🎉 ¡LIMPIADO COMPLETADO!")