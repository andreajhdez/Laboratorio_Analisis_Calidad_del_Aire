import pandas as pd
import sqlite3

# Conectar a la base de datos SQLite
conn = sqlite3.connect('demografia_calidad_aire.db')
cursor = conn.cursor()

# Hacer un JOIN entre las tablas de demografía y calidad del aire
query = '''
SELECT 
    demografia.City, 
    demografia.`Total Population` AS Population,
    calidad_aire.CO,
    calidad_aire.PM10,
    calidad_aire.SO2,
    calidad_aire.`PM2.5`,
    calidad_aire.O3,
    calidad_aire.NO2
FROM 
    demografia
JOIN 
    calidad_aire
ON 
    demografia.City = calidad_aire.City
ORDER BY 
    Population DESC
LIMIT 10;
'''

# Ejecutar la consulta y obtener los resultados
df_resultado = pd.read_sql_query(query, conn)

print("\nLas 10 ciudades más pobladas con sus concentraciones de calidad del aire:")
print(df_resultado)

# Calcular la media de cada contaminante
promedios_calidad_aire = df_resultado[['CO', 'PM10', 'SO2', 'PM2.5', 'O3', 'NO2']].mean()
print("\nPromedio de las concentraciones de calidad del aire en las 10 ciudades más pobladas:")
print(promedios_calidad_aire)

# Cerrar la conexión a la base de datos
conn.close()
