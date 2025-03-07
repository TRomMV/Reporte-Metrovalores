import pandas as pd
import os

def obtener_dividendos():
    # Ruta del archivo CSV (relativa al archivo actual)
    archivo_csv = os.path.join(os.path.dirname(__file__), 'tablas_juntas_2024.csv')

    # Verificar si el archivo existe
    if not os.path.exists(archivo_csv):
        raise FileNotFoundError(f"El archivo {archivo_csv} no existe. Verifica la ruta y el archivo.")
    # Leer el archivo CSV y procesar los datos
    try:
        df = pd.read_csv(archivo_csv, sep=';', decimal=',', encoding='utf-8')
    except Exception as e:
        raise ValueError(f"Error al leer el archivo CSV: {e}")

    # Reemplazar valores vacíos o nulos con el símbolo "-"
    df.fillna('-', inplace=True)

    # Limpiar columnas de posibles espacios en los encabezados
    df.columns = df.columns.str.strip()

    # Convertir a una lista de diccionarios para que sea más fácil de manejar en la aplicación
    dividendos = df.to_dict(orient='records')

    return dividendos
