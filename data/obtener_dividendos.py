import pandas as pd
import os

def obtener_dividendos():
    # Usar una ruta relativa al archivo actual
    archivo_csv = os.path.join(os.path.dirname(__file__), 'tablas_juntas_2024.csv')

    # Verificar si el archivo existe
    if not os.path.exists(archivo_csv):
        raise FileNotFoundError(f"El archivo {archivo_csv} no existe. Verifica la ruta y el archivo.")

    # Leer el archivo CSV
    try:
        df = pd.read_csv(archivo_csv, sep=';', encoding='utf-8')  # Ajusta el separador y codificación si es necesario
    except pd.errors.EmptyDataError:
        raise ValueError(f"El archivo {archivo_csv} está vacío.")
    except pd.errors.ParserError:
        raise ValueError(f"Error al analizar el archivo {archivo_csv}. Verifica el formato.")
    except Exception as e:
        raise ValueError(f"Error desconocido al leer el archivo CSV: {e}")
    
    # Limpieza y procesamiento de los datos
    df.columns = df.columns.str.strip()  # Eliminar espacios adicionales en encabezados
    df['Empresa'] = df['Empresa'].str.strip()  # Eliminar espacios en nombres de empresas

    # Filtrar las empresas de interés
    empresas = ['BANCO GUAYAQUIL S.A.', 'BANCO PICHINCHA C.A.']
    df_filtrado = df[df['Empresa'].isin(empresas)]

    # Verificar si hay datos después del filtrado
    if df_filtrado.empty:
        print("No se encontraron datos para las empresas especificadas.")
        return []

    # Convertir a diccionario para facilitar su uso
    dividendos_dict = df_filtrado.to_dict(orient='records')
    print("Datos de dividendos procesados:", dividendos_dict)  # Debug para logs
    return dividendos_dict
