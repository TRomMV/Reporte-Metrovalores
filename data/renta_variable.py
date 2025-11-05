import pandas as pd
from datetime import datetime

def obtener_datos_renta_variable():
    hoy = datetime.now()

    # Verificar si hoy es lunes y usar el archivo correspondiente
    if hoy.weekday() == 0:  # 0 = lunes
        datos_actualizados_path = 'data/datos_actualizados_lunes.csv'
    else:
        datos_actualizados_path = 'data/datos_actualizados.csv'
    
    df = pd.read_csv(datos_actualizados_path)

    # Asegurarse de que todas las columnas necesarias estén presentes
    columnas_necesarias = ['VARIACION_SEMANAL', 'PRECIO_FINAL', 'PRECIO_INICIAL', 'PRECIO_CIERRE_2024', 'FECHA_ULTIMA_TRANSACCION', 'FECHA_SEMANA_ANTERIOR', 'SECTOR']
    for columna in columnas_necesarias:
        if columna not in df.columns:
            df[columna] = "N/A"

    df['VARIACION_SEMANAL'] = df['VARIACION_SEMANAL'].astype(str)
    df['PRECIO_FINAL'] = df['PRECIO_FINAL'].astype(str)
    df['PRECIO_INICIAL'] = df['PRECIO_INICIAL'].astype(str)
    df['PRECIO_CIERRE_2024'] = df['PRECIO_CIERRE_2024'].astype(str)
    df['FECHA_ULTIMA_TRANSACCION'] = df['FECHA_ULTIMA_TRANSACCION'].astype(str)
    df['FECHA_SEMANA_ANTERIOR'] = df['FECHA_SEMANA_ANTERIOR'].astype(str)
    df['SECTOR'] = df['SECTOR'].astype(str)

    return df.to_dict(orient='records')
