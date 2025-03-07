import pandas as pd

# Ruta absoluta del archivo CSV
archivo_csv = r'C:\Users\tomas\Desktop\MetrovaloresApp\data\tablas_juntas_2024.csv'

try:
    # Leer el archivo CSV
    datos = pd.read_csv(archivo_csv, sep=';', decimal=',', encoding='utf-8', header=1)
    print("El archivo CSV fue leído correctamente. Aquí están las primeras filas:")
    print(datos.head())  # Muestra las primeras 5 filas
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
