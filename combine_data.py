import pandas as pd
import os

# Definir los nombres de las columnas esperados para todos los archivos
column_names = [
    'FECHA', 'EMISOR', 'VALOR', 'VALOR NOMINAL', 'PRECIO', 'NUMERO ACCIONES', 'VALOR EFECTIVO', 'PROCEDENCIA'
]

# Leer el archivo .csv con los datos de 2019 a 2022 usando skiprows para evitar filas innecesarias
file_path_2019_2023 = 'data/BVG-acciones.csv'
df_2019_2023 = pd.read_csv(file_path_2019_2023, encoding='latin1', skiprows=9, names=column_names)

# Eliminar columnas innecesarias (si existen)
df_2019_2023 = df_2019_2023.loc[:, ~df_2019_2023.columns.str.contains('^Unnamed')]

# Leer los archivos .csv con los datos de 2024 y 2025 sin skiprows
file_path_2024 = 'data/acciones_2024.csv'
file_path_2025 = 'data/acciones_2025.csv'
df_2024 = pd.read_csv(file_path_2024, encoding='latin1')
df_2025 = pd.read_csv(file_path_2025, encoding='latin1')

# Eliminar columnas innecesarias (si existen)
df_2024 = df_2024.loc[:, ~df_2024.columns.str.contains('^Unnamed')]
df_2025 = df_2025.loc[:, ~df_2025.columns.str.contains('^Unnamed')]

# Limpiar los datos
def clean_data(df, date_column):
    df.columns = df.columns.str.strip().str.upper()  # Asegurarse de que las columnas estén en mayúsculas
    df[date_column] = pd.to_datetime(df[date_column], format='%d/%m/%Y', errors='coerce')
    df = df.dropna(subset=[date_column])
    df.loc[:, 'PRECIO'] = df['PRECIO'].apply(lambda x: str(x).replace(',', '')).astype(float, errors='ignore')
    return df

# Limpiar los DataFrames
df_2019_2023 = clean_data(df_2019_2023, 'FECHA')
df_2024 = clean_data(df_2024, 'FECHA')
df_2025 = clean_data(df_2025, 'FECHA')

# Filtrar los datos para incluir solo las filas con 'ACCIONES' o 'ACCIONES PREFERIDAS' en la columna 'VALOR'
df_2019_2023 = df_2019_2023[df_2019_2023['VALOR'].str.strip().str.upper().isin(['ACCIONES', 'ACCIONES PREFERIDAS'])]
df_2024 = df_2024[df_2024['VALOR'].str.strip().str.upper().isin(['ACCIONES', 'ACCIONES PREFERIDAS'])]
df_2025 = df_2025[df_2025['VALOR'].str.strip().str.upper().isin(['ACCIONES', 'ACCIONES PREFERIDAS'])]

# Renombrar columnas para que coincidan en todos los DataFrames
df_2019_2023 = df_2019_2023.rename(columns={'NUMERO ACCIONES': 'ACCIONES'})
df_2024 = df_2024.rename(columns={'VALOR NOMINAL': 'VALOR NOMINAL', 'NUMERO ACCIONES': 'ACCIONES'})
df_2025 = df_2025.rename(columns={'VALOR NOMINAL': 'VALOR NOMINAL', 'NUMERO ACCIONES': 'ACCIONES'})

# Seleccionar columnas comunes
common_columns = ['FECHA', 'EMISOR', 'PRECIO', 'VALOR NOMINAL', 'ACCIONES', 'VALOR EFECTIVO', 'PROCEDENCIA']
df_2019_2023 = df_2019_2023[common_columns]
df_2024 = df_2024[common_columns]
df_2025 = df_2025[common_columns]

# Filtrar empresas de interés para 2019 a 2023
empresas_interes_2019_2023 = df_2019_2023['EMISOR'].unique()

# Filtrar empresas de interés para 2024 y 2025, incluyendo INDUSTRIAS ALES
empresas_interes = list(empresas_interes_2019_2023)
if 'INDUSTRIAS ALES' not in empresas_interes:
    empresas_interes.append('INDUSTRIAS ALES')

df_2024 = df_2024[df_2024['EMISOR'].isin(empresas_interes)]
df_2025 = df_2025[df_2025['EMISOR'].isin(empresas_interes)]

# Conservar solo el último registro de cada día
df_2019_2023 = df_2019_2023.sort_values(by='FECHA').drop_duplicates(subset=['FECHA', 'EMISOR'], keep='last')
df_2024 = df_2024.sort_values(by='FECHA').drop_duplicates(subset=['FECHA', 'EMISOR'], keep='last')
df_2025 = df_2025.sort_values(by='FECHA').drop_duplicates(subset=['FECHA', 'EMISOR'], keep='last')

# Unir todos los datos
combined_df = pd.concat([df_2019_2023, df_2024, df_2025], ignore_index=True)

# Verificar si el archivo existe y eliminarlo antes de escribir
combined_csv_path = 'data/acciones_combinadas.csv'
if os.path.exists(combined_csv_path):
    os.remove(combined_csv_path)

# Guardar el DataFrame combinado como CSV
combined_df.to_csv(combined_csv_path, index=False)

print('Datos combinados correctamente.')
