import pandas as pd
import os

def obtener_dividendos():
    """
    Lee y procesa el archivo CSV de dividendos, limpiando y preparando los datos
    para ser utilizados en la aplicación.
    """
    # Ruta relativa al archivo CSV
    archivo_csv = os.path.join(os.path.dirname(__file__), 'tablas_juntas_2024.csv')

    try:
        # Leer el CSV con configuración apropiada
        datos = pd.read_csv(archivo_csv, sep=';', decimal=',', encoding='utf-8')
    except Exception as e:
        raise ValueError(f"Error al leer el archivo CSV: {e}")

    # Limpiar encabezados y valores
    datos.columns = datos.columns.str.strip()  # Limpiar espacios en los nombres de las columnas
    datos['Empresa'] = datos['Empresa'].str.strip()  # Limpiar espacios en los nombres de las empresas

    # Reemplazar celdas vacías o nulas con un símbolo "-"
    datos.fillna('-', inplace=True)

    # Asegurarse de que valores numéricos estén formateados adecuadamente
    for columna in ['Capital (miles)', 'Utilidad Neta (miles)', 'Dividendo en efectivo (miles)',
                    'Dividendo en efectivo por accion', 'Aumento capital (miles)',
                    'Aumento de capital por accion', 'Ultimo precio', 'Rendimiento del dividendo (Yield)']:
        if columna in datos.columns:
            datos[columna] = datos[columna].astype(str).str.replace(' ', '').str.replace('$', '').str.replace('%', '').str.replace(',', '.')
            datos[columna] = pd.to_numeric(datos[columna], errors='coerce').fillna('-')

    # Convertir a una lista de diccionarios para uso en Flask
    dividendos = datos.to_dict(orient='records')

    return dividendos
