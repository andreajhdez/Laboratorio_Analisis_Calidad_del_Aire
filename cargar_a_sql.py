import pandas as pd
import sqlite3

# Leer los archivos CSV guardados
us_demographics = pd.read_csv('demografia_df.csv')
df_calidad_aire = pd.read_csv('calidad_aire_df.csv')

# Crear una conexión a la base de datos SQLite
conn = sqlite3.connect('demografia_calidad_aire.db')  # Si la base de datos no existe, se creará
cursor = conn.cursor()

# Crear tablas y cargar los datos
us_demographics.to_sql('demografia', conn, if_exists='replace', index=False)
df_calidad_aire.to_sql('calidad_aire', conn, if_exists='replace', index=False)

print("\nDatos cargados en la base de datos SQLite correctamente.")

# Verificar que las tablas se hayan creado y cargado correctamente
print("\nTablas en la base de datos SQLite:")
for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(row[0])

print("\nPrimeras 5 filas de la tabla 'demografia':")
print(pd.read_sql_query("SELECT * FROM demografia LIMIT 5;", conn))

print("\nPrimeras 5 filas de la tabla 'calidad_aire':")
print(pd.read_sql_query("SELECT * FROM calidad_aire LIMIT 5;", conn))

# Cerrar la conexión a la base de datos
conn.close()