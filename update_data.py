import requests
import pandas as pd
import os

# URL del archivo .xls en la Bolsa de Valores de Quito
url = 'https://www.bolsadequito.com/uploads/estadisticas/boletines/cotizaciones-historicas/acciones.xls'

# Establecer los headers para la solicitud HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Crear la carpeta 'data' si no existe
if not os.path.exists('data'):
    os.makedirs('data')

# Descargar el archivo .xls con los headers
response = requests.get(url, headers=headers)
file_path = 'data/acciones.xls'

with open(file_path, 'wb') as file:
    file.write(response.content)

# Verificar si el archivo se descargó correctamente
if not os.path.exists(file_path):
    print("Error: El archivo no se descargó correctamente.")
    exit()

# Leer el archivo .xls y separar las hojas usando xlrd
try:
    df_2024 = pd.read_excel(file_path, sheet_name='2024', header=8, engine='xlrd')
    df_2025 = pd.read_excel(file_path, sheet_name='2025', header=8, engine='xlrd')
except Exception as e:
    print("Error al leer el archivo Excel:", e)
    exit()

# Limpiar los datos
def clean_data(df):
    df.columns = df.columns.str.strip().str.upper()  # Asegurarse de que las columnas estén en mayúsculas
    df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
    df = df.dropna(subset=['FECHA'])
    df['PRECIO'] = df['PRECIO'].apply(lambda x: str(x).replace(',', '')).astype(float, errors='ignore')
    df['PROCEDENCIA'] = df['PROCEDENCIA'].replace({'G': 'BVG', 'Q': 'BVQ'})
    return df

df_2024 = clean_data(df_2024)
df_2025 = clean_data(df_2025)

# Leer el archivo combinado para obtener la lista de empresas de interés
acciones_combinadas_path = 'data/acciones_combinadas.csv'
if os.path.exists(acciones_combinadas_path):
    df_combinado = pd.read_csv(acciones_combinadas_path)
    empresas_interes = df_combinado['EMISOR'].unique()
    empresas_interes = list(empresas_interes)
else:
    empresas_interes = []

# Asegurarse de que INDUSTRIAS ALES, CONTINENTAL e INVERSANCARLOS estaN incluidas en empresas de interés
if 'CONTINENTAL TIRE ANDINA S.A.' not in empresas_interes:
    empresas_interes.append('CONTINENTAL TIRE ANDINA S A')
if 'INDUSTRIAS ALES C.A.' not in empresas_interes:
    empresas_interes.append('INDUSTRIAS ALES')
if 'INVERSANCARLOS S.A.' not in empresas_interes:
    empresas_interes.append('INVERSANCARLOS')
if 'BANCO DEL AUSTRO' not in empresas_interes:
    empresas_interes.append('BANCO DEL AUSTRO')
if 'BRIKAPITAL SA' not in empresas_interes:
    empresas_interes.append('BRIKAPITAL SA')
if 'CRIDESA' not in empresas_interes:
    empresas_interes.append('CRIDESA')

# Filtrar los datos para incluir solo las empresas de interés
df_2024 = df_2024[df_2024['EMISOR'].isin(empresas_interes)]
df_2025 = df_2025[df_2025['EMISOR'].isin(empresas_interes)]

# Eliminar archivos CSV existentes si existen
if os.path.exists('data/acciones_2024.csv'):
    os.remove('data/acciones_2024.csv')
if os.path.exists('data/acciones_2025.csv'):
    os.remove('data/acciones_2025.csv')

# Guardar los datos como archivos CSV
df_2024.to_csv('data/acciones_2024.csv', index=False)
df_2025.to_csv('data/acciones_2025.csv', index=False)

print('Datos actualizados correctamente.')
