import pandas as pd

def cargar_datos(ruta_csv):
    """
    Carga los datos del archivo CSV en un DataFrame de pandas.
    """
    datos = pd.read_csv(ruta_csv)
    datos['FECHA'] = pd.to_datetime(datos['FECHA'], errors='coerce')  # Asegurarse de que la columna FECHA esté en formato datetime
    return datos

def calcular_indices(datos, año):
    """
    Calcula los índices financieros necesarios para un año específico.
    """
    datos_año = datos[datos['FECHA'].dt.year == año]
    
    if datos_año.empty:
        # Manejar casos donde no hay datos disponibles
        return {
            'acciones_total': 0,
            'precio_apertura': None,
            'precio_cierre': None
        }

    acciones_total = datos_año['ACCIONES'].sum()
    precio_apertura = datos_año.iloc[0]['PRECIO']
    precio_cierre = datos_año.iloc[-1]['PRECIO']

    indices = {
        'acciones_total': acciones_total,
        'precio_apertura': precio_apertura,
        'precio_cierre': precio_cierre
    }

    return indices

def obtener_datos_empresa(empresa, datos):
    """
    Filtra los datos para obtener solo los registros de la empresa especificada.
    """
    datos_empresa = datos[datos['EMISOR'] == empresa]
    return datos_empresa

def procesar_datos_empresa(ruta_csv, empresa):
    """
    Procesa los datos para una empresa específica y calcula los índices.
    """
    datos = cargar_datos(ruta_csv)
    datos_empresa = obtener_datos_empresa(empresa, datos)
    indices = calcular_indices(datos_empresa, 2024)
    return indices
