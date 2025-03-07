import pandas as pd

def cargar_datos_dividendos():
    """
    Carga los datos del archivo CSV desde una ruta absoluta y realiza limpieza y validación básica.
    """
    # Ruta absoluta al archivo CSV
    ruta_csv = r'C:\Users\tomas\Desktop\MetrovaloresApp\data\tablas_juntas_2024.csv'

    try:
        # Leer el archivo CSV con las configuraciones adecuadas
        datos = pd.read_csv(ruta_csv, sep=';', decimal=',', encoding='utf-8', header=1)

        # Validar y normalizar columnas necesarias
        columnas_necesarias = [
            'Año', 'Capital (miles)', 'Utilidad Neta (miles)', 
            'Dividendo en efectivo (miles)', 'Dividendo en efectivo por accion', 
            'Aumento capital (miles)', 'Aumento de capital por accion', 
            'Ultimo precio', 'Rendimiento del dividendo (Yield)', 'Empresa'
        ]
        
        for columna in columnas_necesarias:
            if columna not in datos.columns:
                datos[columna] = "N/A"  # Completar columnas faltantes con valores predeterminados

        # Normalizar encabezados y datos en 'Empresa'
        datos.columns = datos.columns.str.strip()  # Limpiar espacios en los encabezados
        datos['Empresa'] = datos['Empresa'].str.upper().str.strip()  # Normalizar nombres de empresas

        # Convertir valores a cadenas para evitar problemas de representación
        for columna in columnas_necesarias:
            if columna in datos.columns:
                datos[columna] = datos[columna].astype(str)

        return datos
    except Exception as e:
        # Manejo de errores al leer el CSV
        raise ValueError(f"Error al leer el archivo CSV: {e}")

def obtener_datos_emisor(emisor, datos):
    """
    Filtra los datos para obtener solo los registros del emisor especificado.
    """
    # Asegurarse de que el emisor esté en mayúsculas y limpio
    datos_emisor = datos[datos['Empresa'] == emisor.upper()]
    return datos_emisor

def procesar_dividendos_emisor(emisor):
    """
    Carga y procesa los datos para un emisor específico.
    """
    # Cargar los datos desde el CSV
    datos = cargar_datos_dividendos()

    # Filtrar por el emisor solicitado
    dividendos_emisor = obtener_datos_emisor(emisor, datos)

    # Convertir a lista de diccionarios para facilitar su uso en la plantilla HTML
    return dividendos_emisor.to_dict(orient='records')
