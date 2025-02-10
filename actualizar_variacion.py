import pandas as pd
from datetime import datetime, timedelta

# Leer los datos desde el archivo CSV
acciones_combinadas_path = 'data/acciones_combinadas.csv'
df = pd.read_csv(acciones_combinadas_path)

# Limpiar los datos
df.columns = df.columns.str.strip().str.upper()
df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
df = df.dropna(subset=['FECHA'])

# Filtrar por precio de cierre
df = df[df['PRECIO'].notnull()]

# Definir los sectores de las empresas
sector_financiero = [
    'BANCO GUAYAQUIL S.A.', 'BANCO DE LA PRODUCCION S.A . PRODUBANCO',
    'BANCO PICHINCHA C.A.', 'BANCO BOLIVARIANO C.A.',
    'BOLSA DE VALORES DE GUAYAQUIL', 'BOLSA DE VALORES DE QUITO'
]
sector_real = [
    'CORPORACION FAVORITA C.A.', 'CERVECERIA NACIONAL CN S A',
    'HOLCIM ECUADOR S.A.', 'SAN CARLOS SOC. AGR. IND.'
]

# Añadir la columna de sector
df['SECTOR'] = df['EMISOR'].apply(lambda x: 'Financiero' if x in sector_financiero else 'Real')

def obtener_ultimo_precio(grupo):
    """Obtener el último precio y fecha disponibles para la empresa."""
    ultimo = grupo.sort_values(by='FECHA').iloc[-1]
    return pd.Series([ultimo['FECHA'], ultimo['PRECIO']], index=['FECHA', 'PRECIO'])

def obtener_precio_semana_anterior(grupo, lunes_anterior, viernes_anterior):
    """Obtener el precio de cierre de la semana anterior."""
    semana_anterior = grupo[(grupo['FECHA'] >= lunes_anterior) & (grupo['FECHA'] <= viernes_anterior)]
    if not semana_anterior.empty:
        ultimo = semana_anterior.sort_values(by='FECHA').iloc[-1]
        return pd.Series([ultimo['FECHA'], ultimo['PRECIO']], index=['FECHA', 'PRECIO'])
    return pd.Series([None, None], index=['FECHA', 'PRECIO'])

def obtener_precio_cierre_2024(grupo):
    """Obtener el precio de cierre del último día hábil de 2024."""
    cierre_2024 = grupo[grupo['FECHA'].dt.year == 2024].sort_values(by='FECHA').iloc[-1]
    return pd.Series([cierre_2024['FECHA'], cierre_2024['PRECIO']], index=['FECHA', 'PRECIO_CIERRE_2024'])

def obtener_fechas_semana():
    hoy = datetime.now()
    lunes_actual = hoy - timedelta(days=hoy.weekday())
    lunes_anterior = lunes_actual - timedelta(days=7)
    return lunes_anterior, lunes_actual

def actualizar_variacion_semanal():
    lunes_anterior, lunes_actual = obtener_fechas_semana()
    viernes_actual = lunes_actual + timedelta(days=4)
    viernes_anterior = lunes_anterior + timedelta(days=4)

    todas_las_empresas = df['EMISOR'].unique()

    precios_ultimos = df.groupby('EMISOR').apply(obtener_ultimo_precio, include_groups=False).reset_index()
    precios_ultimos.columns = ['EMISOR', 'FECHA_ULTIMA_TRANSACCION', 'PRECIO_FINAL']
    precios_ultimos = precios_ultimos.set_index('EMISOR')
    precios_ultimos['FECHA_ULTIMA_TRANSACCION'] = pd.to_datetime(precios_ultimos['FECHA_ULTIMA_TRANSACCION']).dt.strftime('%Y-%m-%d')

    precios_semana_anterior = df.groupby('EMISOR').apply(lambda x: obtener_precio_semana_anterior(x, lunes_anterior, viernes_anterior), include_groups=False).reset_index()
    precios_semana_anterior.columns = ['EMISOR', 'FECHA_SEMANA_ANTERIOR', 'PRECIO_INICIAL']
    precios_semana_anterior = precios_semana_anterior.set_index('EMISOR')
    precios_semana_anterior['FECHA_SEMANA_ANTERIOR'] = pd.to_datetime(precios_semana_anterior['FECHA_SEMANA_ANTERIOR']).dt.strftime('%Y-%m-%d')

    precios_cierre_2024 = df.groupby('EMISOR').apply(obtener_precio_cierre_2024, include_groups=False).reset_index()
    precios_cierre_2024.columns = ['EMISOR', 'FECHA_CIERRE_2024', 'PRECIO_CIERRE_2024']
    precios_cierre_2024 = precios_cierre_2024.set_index('EMISOR')
    precios_cierre_2024['FECHA_CIERRE_2024'] = pd.to_datetime(precios_cierre_2024['FECHA_CIERRE_2024']).dt.strftime('%Y-%m-%d')

    datos_renta_variable = precios_ultimos.join(precios_semana_anterior, how='left').join(precios_cierre_2024, how='left')
    datos_renta_variable = datos_renta_variable.reindex(todas_las_empresas).drop_duplicates()

    datos_renta_variable['VARIACION_SEMANAL'] = (
        (datos_renta_variable['PRECIO_FINAL'].astype(float) - datos_renta_variable['PRECIO_INICIAL'].astype(float)) / datos_renta_variable['PRECIO_INICIAL'].astype(float)
    ) * 100
    datos_renta_variable['VARIACION_SEMANAL'] = datos_renta_variable['VARIACION_SEMANAL'].fillna(0)

    datos_renta_variable['VARIACION_SEMANAL'] = datos_renta_variable['VARIACION_SEMANAL'].apply(lambda x: f"{x:.2f}%")
    datos_renta_variable['PRECIO_FINAL'] = datos_renta_variable['PRECIO_FINAL'].apply(lambda x: f"${x:,.2f}")
    datos_renta_variable['PRECIO_INICIAL'] = datos_renta_variable['PRECIO_INICIAL'].apply(lambda x: f"${x:,.2f}")
    datos_renta_variable['PRECIO_CIERRE_2024'] = datos_renta_variable['PRECIO_CIERRE_2024'].apply(lambda x: f"${x:,.2f}")

    # Añadir la columna de sector a los datos finales
    datos_renta_variable['SECTOR'] = df.drop_duplicates(subset=['EMISOR']).set_index('EMISOR')['SECTOR']

    # Guardar todos los datos en un archivo CSV
    datos_renta_variable.to_csv('data/datos_actualizados.csv', index=True)

    print("Actualización completada: Los datos se han guardado correctamente en 'data/datos_actualizados.csv'.")

actualizar_variacion_semanal()

