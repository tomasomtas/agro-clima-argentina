# clima_downloader.py
# Descarga datos climáticos de Argentina usando Open-Meteo

import openmeteo_requests
import requests_cache
import pandas as pd
import os          # 👈 agregar esta línea
import time        # 👈 y esta, para el sleep() de antes
from retry_requests import retry


# Configurar caché y reintentos
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Provincias argentinas con coordenadas aproximadas
provincias = {
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
}

import time
from openmeteo_requests.Client import OpenMeteoRequestsError

def descargar_clima(provincia, lat, lon, start_date="2010-01-01", end_date="2024-12-31", max_reintentos=5):
    """Descarga datos climáticos para una provincia usando Open-Meteo, con reintento automático"""
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "precipitation_sum",
            "rain_sum",
            "sunshine_duration",
            "wind_speed_10m_max",
            "et0_fao_evapotranspiration"
        ],
        "timezone": "America/Argentina/Buenos_Aires"
    }
    
    print(f"📥 Descargando datos para {provincia}...")
    
    for intento in range(1, max_reintentos + 1):
        try:
            responses = openmeteo.weather_api(url, params=params)
            break  # si funciona, salimos del for
        except OpenMeteoRequestsError as e:
            if "limit" in str(e).lower() and intento < max_reintentos:
                espera = 65  # esperamos un poco más de 1 minuto
                print(f"⏳ Límite de API alcanzado, esperando {espera}s (intento {intento}/{max_reintentos})...")
                time.sleep(espera)
            else:
                raise  # si no es error de límite, o se agotaron los intentos, lo tiramos para arriba
    
    response = responses[0]
    
    # ... el resto de la función queda igual (procesar daily_data, etc.)
    
    # Procesar datos diarios
    # Procesar datos diarios
    daily = response.Daily()
    daily_data = {
    "date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True).tz_convert("America/Argentina/Buenos_Aires"),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True).tz_convert("America/Argentina/Buenos_Aires"),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"   # 👈 esto es lo que falta
    ),
    "temp_max": daily.Variables(0).ValuesAsNumpy(),
    "temp_min": daily.Variables(1).ValuesAsNumpy(),
    "temp_mean": daily.Variables(2).ValuesAsNumpy(),
    "precipitacion": daily.Variables(3).ValuesAsNumpy(),
    "lluvia": daily.Variables(4).ValuesAsNumpy(),
    "horas_sol": daily.Variables(5).ValuesAsNumpy(),
    "viento_max": daily.Variables(6).ValuesAsNumpy(),
    "evapotranspiracion": daily.Variables(7).ValuesAsNumpy()
}  
    
    # Crear el DataFrame con los datos diarios
    df = pd.DataFrame(daily_data)
    
    # Agregar las columnas de provincia y coordenadas (Pandas repite el valor para todas las filas)
    df["provincia"] = provincia
    df["lat"] = lat
    df["lon"] = lon
    
    return df

import time

def main():
    """Descarga datos para todas las provincias y los guarda"""
    os.makedirs("data", exist_ok=True)
    todos = []
    
    for provincia, coords in provincias.items():
        df = descargar_clima(provincia, coords["lat"], coords["lon"])
        todos.append(df)
        time.sleep(10)  # 👈 más margen entre provincias
    
    df_final = pd.concat(todos, ignore_index=True)
    df_final.to_csv("data/clima_argentina.csv", index=False, encoding="utf-8-sig")
    
    print(f"\n✅ Datos guardados en data/clima_argentina.csv")
    print(f"📊 Registros: {len(df_final):,}")
    print(f"📅 Desde {df_final['date'].min()} hasta {df_final['date'].max()}")
    print(f"📋 Columnas: {df_final.columns.tolist()}")

if __name__ == "__main__":
    main() 
    