import pandas as pd

# Ruta absoluta del archivo CSV
ruta_csv = r'C:\Users\tomas\Desktop\MetrovaloresApp\data\tablas_juntas_2024.csv'

try:
    # Leer el archivo CSV y usar la primera fila como encabezados
    datos = pd.read_csv(ruta_csv, sep=';', decimal=',', encoding='utf-8', header=0)

    # Imprimir todas las columnas encontradas en el CSV
    print("Columnas encontradas en el CSV:")
    print(datos.columns.tolist())  # Lista los títulos reales de las columnas

    # Mostrar las primeras filas de datos
    print("\nPrimeras filas del CSV:")
    print(datos.head())

except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
