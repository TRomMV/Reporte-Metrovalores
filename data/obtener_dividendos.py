import pandas as pd

def cargar_datos_dividendos():
    """
    Carga los datos del archivo CSV desde una ruta absoluta y realiza limpieza básica.
    """
    # Ruta absoluta al archivo CSV
    ruta_csv = r'C:\Users\tomas\Desktop\MetrovaloresApp\data\tablas_juntas_2024.csv'

    try:
        # Leer el archivo CSV con las configuraciones adecuadas
        datos = pd.read_csv(ruta_csv, sep=';', decimal=',', encoding='utf-8', header=0)

        # Limpiar columnas y normalizar nombres
        datos.columns = datos.columns.str.strip()
        datos['Empresa'] = datos['Empresa'].str.upper().str.strip()

        return datos
    except Exception as e:
        raise ValueError(f"Error al leer el archivo CSV: {e}")

def obtener_datos_emisor(emisor, datos):
    """
    Filtra los datos para obtener solo los registros del emisor especificado.
    """
    # Filtrar los datos por empresa
    datos_emisor = datos[datos['Empresa'] == emisor.upper()]
    return datos_emisor

def procesar_dividendos_emisor(ruta_csv, emisor):
    """
    Carga y procesa los datos para un emisor específico.
    """
    # Cargar todos los datos desde el CSV
    datos = cargar_datos_dividendos()

    # Filtrar por el emisor solicitado
    dividendos_emisor = obtener_datos_emisor(emisor, datos)

    # Depuración: Imprimir los datos filtrados
    print(f"Datos filtrados para {emisor}: {dividendos_emisor}")

    # Convertir a lista de diccionarios para facilitar su uso en la plantilla HTML
    return dividendos_emisor.to_dict(orient='records')

