import pandas as pd

def obtener_dividendos():
    # Ruta del archivo CSV
    archivo_csv = 'C:/Users/tomas/Desktop/MetrovaloresApp/data/tablas_juntas_2024.csv'
    
    # Leer el archivo CSV
    df = pd.read_csv(archivo_csv, sep=',')  # Asegúrate de que el separador sea correcto

    # Filtrar solo las filas correspondientes a las empresas específicas
    empresas = ['BANCO GUAYAQUIL S.A.', 'BANCO PICHINCHA C.A.', 'BANCO BOLIVARIANO C.A.']
    df_empresas = df[df['Empresa'].isin(empresas)]  # Asegúrate de que la columna 'Empresa' exista

    # Convertir el DataFrame a un diccionario para facilitar su uso en la plantilla
    dividendos_dict = df_empresas.to_dict(orient='records')

    return dividendos_dict