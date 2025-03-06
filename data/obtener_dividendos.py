import pandas as pd
import os

def obtener_dividendos():
    # Ruta del archivo CSV
    archivo_csv = 'C:/Users/tomas/Desktop/MetrovaloresApp/data/tablas_juntas_2024.csv'
    
    # Verificar si el archivo existe
    if not os.path.exists(archivo_csv):
        raise FileNotFoundError(f"El archivo {archivo_csv} no existe. Verifica la ruta y el archivo.")

    # Leer el archivo CSV
    try:
        df = pd.read_csv(archivo_csv, sep=';')  # Asegúrate de usar el separador correcto (cámbialo si no es ';')
    except pd.errors.EmptyDataError:
        raise ValueError(f"El archivo {archivo_csv} está vacío.")
    except pd.errors.ParserError:
        raise ValueError(f"Error al analizar el archivo {archivo_csv}. Verifica el formato.")
    except Exception as e:
        raise ValueError(f"Error desconocido al leer el archivo CSV: {e}")
    
    # Asegurar que la columna 'Empresa' existe y limpiar valores innecesarios
    if 'Empresa' not in df.columns:
        raise KeyError("La columna 'Empresa' no existe en el archivo CSV. Verifica los encabezados.")

    # Eliminar espacios en blanco o inconsistencias en los nombres de las empresas
    df['Empresa'] = df['Empresa'].str.strip()

    # Filtrar solo las filas correspondientes a las empresas específicas
    empresas = ['BANCO GUAYAQUIL S.A.', 'BANCO PICHINCHA C.A.', 'BANCO BOLIVARIANO C.A.']
    df_empresas = df[df['Empresa'].isin(empresas)]  # Filtrar datos por las empresas de interés

    # Verificar si hay datos después del filtrado
    if df_empresas.empty:
        print("No se encontraron datos para las empresas especificadas.")  # Mensaje de depuración
        return []  # Devuelve una lista vacía si no hay datos para estas empresas

    # Convertir el DataFrame a un diccionario para facilitar su uso en la plantilla
    dividendos_dict = df_empresas.to_dict(orient='records')

    # Imprimir los datos para depuración
    print("Datos Filtrados:", dividendos_dict)

    return dividendos_dict
