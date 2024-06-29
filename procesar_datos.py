import pandas as pd
from typing import Set
import requests
import time
import sqlite3

# PUNTO 1: Cargar datos demográficos
url = "https://public.opendatasoft.com/explore/dataset/us-cities-demographics/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B"
us_demographics = pd.read_csv(url, sep=';')

# PUNTO 3: Eliminar columnas no deseadas y duplicados
us_demographics = us_demographics.drop(
    columns=['Race', 'Count', 'Number of Veterans'])
us_demographics = us_demographics.drop_duplicates()

print("Datos demográficos de EE.UU.:")
print(us_demographics)

# Lista de ciudades desde el DataFrame de datos demográficos
ciudades = us_demographics['City']

# PUNTO 3: Obtener datos de calidad del aire por ciudad
data_calidad_aire = []

# PUNTO 2: Parsea los datos de calidad del aire para cada ciudad en la tabla demográfica obteniendo la información con la API.
# Crear una tabla con dimensiones usando pandas


def ej_2_cargar_calidad_aire(ciudades):

    for ciudad in ciudades:
        api_url = f'https://api.api-ninjas.com/v1/airquality?city={ciudad}'
        headers = {'X-API-Key': 'DozOV1xW4Yr/mXXRYfDetw==dDU2GGeiPQ1X9HHj'}
        response = requests.get(api_url, headers=headers,
                                params={"city": ciudad})
        if response.status_code == 200:
            datos_api = response.json()
            # Obtener las concentraciones de cada parámetro
            concentracion_aire = {key: value.get('concentration') for key, value in datos_api.items(
            ) if key != 'overall_aqi'}
            # Agregar el nombre de la ciudad al diccionario de concentraciones
            concentracion_aire['City'] = ciudad
            data_calidad_aire.append(concentracion_aire)
        else:
            print(
                f"Error recolectando datos de: {ciudad}. Status(código error): {response.status_code}")


# Llamar a la función para obtener los datos de calidad del aire
ej_2_cargar_calidad_aire(us_demographics['City'])

# Convertir a DataFrame
df_calidad_aire = pd.DataFrame(data_calidad_aire)

# Guardar los DataFrames en archivos CSV
us_demographics.to_csv('demografia_df.csv', index=False)
df_calidad_aire.to_csv('calidad_aire_df.csv', index=False)
print("\nArchivos CSV guardados correctamente.")
