from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import plotly.graph_objs as go
import os
from datetime import datetime, timedelta
from data.descripciones_empresas import obtener_descripcion_empresa
from data.sectores_empresas import obtener_sector_empresa
from data.escalas_volumen import obtener_escala_volumen
import subprocess
from data_processing import procesar_datos_empresa
from data.resumen_dividendos import obtener_resumen_dividendos

app = Flask(__name__)

# Llamar al script de actualización de variación semanal
if os.path.exists("actualizar_variacion.py"):
    subprocess.run(["python", "actualizar_variacion.py"])
else:
    print("El archivo 'actualizar_variacion.py' no se encuentra.")

# Ruta de los archivos CSV
datos_actualizados_path = 'data/datos_actualizados.csv'
datos_actualizados_lunes_path = 'data/datos_actualizados_lunes.csv'
acciones_combinadas_path = 'data/acciones_combinadas.csv'  # Archivo de datos de empresas

# Verifica si el archivo existe
if not os.path.exists(acciones_combinadas_path):
    raise FileNotFoundError(f"El archivo {acciones_combinadas_path} no se encuentra. Verifica que los datos están combinados correctamente.")

# Leer los datos desde el archivo combinado
df_empresas = pd.read_csv(acciones_combinadas_path)

# Limpiar los datos de empresas
df_empresas.columns = df_empresas.columns.str.strip().str.upper()  # Asegurarse de que las columnas estén en mayúsculas
if 'FECHA' not in df_empresas.columns or 'EMISOR' not in df_empresas.columns or 'VALOR' not in df_empresas.columns:
    raise KeyError("Las columnas 'FECHA', 'EMISOR' o 'VALOR' no se encuentran en los datos. Verifique que los datos estén en el formato correcto.")

df_empresas['FECHA'] = pd.to_datetime(df_empresas['FECHA'], errors='coerce')
df_empresas = df_empresas.dropna(subset=['FECHA'])

# Filtrar por precio de cierre y tipo de acción
df_empresas = df_empresas[(df_empresas['PRECIO'].notnull()) & (df_empresas['VALOR'] == 'ACCIONES')]

def format_date(date_obj):
    return date_obj.strftime('%d/%m/%Y')

def format_price(price):
    return "{:.2f}".format(price)

@app.route('/')
def home():
    return render_template('index.html')
    

@app.route('/empresa/<company>')
def show_company(company):
    company = company.replace('-', ' ').upper()  # Asegurarse de que el formato del nombre sea correcto
    company_data = df_empresas[df_empresas['EMISOR'] == company]

    if company_data.empty:
        return render_template('empresa.html', company=company, profile={}, max_quotes=[], min_quotes=[], graph="")
    
    # Filtrar por precio de cierre
    company_data_precio = company_data[company_data['PRECIO'].notnull()]

    # Resamplear para mostrar barras de volumen cada 5 días
    company_data_volumen = company_data.set_index('FECHA').resample('5D').sum().reset_index()

    # Crear gráfico de precios con barras de volumen
    fig = go.Figure()

    # Línea de precios
    fig.add_trace(go.Scatter(x=company_data_precio['FECHA'], y=company_data_precio['PRECIO'], mode='lines', name='Precio', line=dict(color='blue')))
    # Inicializar y2_range con un valor predeterminado
    y2_range = [0, 100]

    # Verificar si la columna 'ACCIONES' existe antes de usarla
    if 'ACCIONES' in company_data.columns:
        # Barras de volumen ajustadas según la empresa
        max_acciones = obtener_escala_volumen(company)
        y2_range = [0, max_acciones * 1.1]  # Ajustar el rango con un 10% más para mejorar la visibilidad
        fig.add_trace(go.Bar(x=company_data_volumen['FECHA'], y=company_data_volumen['ACCIONES'], name='Volumen', yaxis='y2', marker=dict(color='rgba(255, 99, 71, 0.6)')))  # Color más suave

    # Configuración de la escala de tiempo
    fecha_inicio_auto = datetime(2024, 1, 1)
    fecha_fin = company_data_precio['FECHA'].max()

    fig.update_layout(
        title=f'Precio y Volumen de {company}',
        xaxis_title='Fecha',
        yaxis_title='Precio',
        yaxis2=dict(
            title='Volumen',
            overlaying='y',
            side='right',
            showgrid=False,
            range=y2_range  # Aplicar el rango ajustado
        ),
        xaxis=dict(
            range=[fecha_inicio_auto, fecha_fin]
        ),
        hovermode='x unified',
        legend=dict(x=0, y=1.2),
        barmode='overlay',
        dragmode='pan'  # Permitir arrastrar el gráfico con el mouse
    )

    # Configuración del gráfico para habilitar el zoom con el scroll del mouse
    config = dict(
        scrollZoom=True,
        displayModeBar=True,
        modeBarButtonsToRemove=['zoom2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'],
        displaylogo=False
    )

    graph = fig.to_html(full_html=False, config=config)
    # Obtener la descripción y el sector de la empresa actual
    descripcion_empresa = obtener_descripcion_empresa(company)
    sector_empresa = obtener_sector_empresa(company)

    profile = {
        "Nombre": company,
        "Descripción": descripcion_empresa,
        "Sector": sector_empresa
    }
    # Calcular los índices financieros utilizando data_processing.py
    try:
        indices_financieros = procesar_datos_empresa(acciones_combinadas_path, company)
    except IndexError:
        indices_financieros = {}  # Manejar el caso donde no hay datos para procesar índices

    # Obtener las cotizaciones máximas y mínimas por año desde 2019 hasta 2024
    años = list(range(2019, 2025))
    max_quotes = []
    min_quotes = []

    for año in años:
        datos_año = company_data[company_data['FECHA'].dt.year == año]
        if not datos_año.empty:
            max_cotizacion = datos_año.loc[datos_año['PRECIO'].idxmax()]
            min_cotizacion = datos_año.loc[datos_año['PRECIO'].idxmin()]
            max_quotes.append({'AÑO': año, 'FECHA': format_date(max_cotizacion['FECHA']), 'PRECIO': format_price(max_cotizacion['PRECIO'])})
            min_quotes.append({'AÑO': año, 'FECHA': format_date(min_cotizacion['FECHA']), 'PRECIO': format_price(min_cotizacion['PRECIO'])})

    # Obtener la cotización máxima y mínima del último mes cerrado
    fecha_actual = datetime.now()
    año_actual = fecha_actual.year
    ultimo_mes_cerrado = (fecha_actual.replace(day=1) - timedelta(days=1)).month
    año_ultimo_mes_cerrado = fecha_actual.year if ultimo_mes_cerrado != 12 else fecha_actual.year - 1

    # Mapeo de los nombres de los meses en inglés a español
    meses = {
        'January': 'enero', 'February': 'febrero', 'March': 'marzo',
        'April': 'abril', 'May': 'mayo', 'June': 'junio',
        'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
        'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
    }

    nombre_mes_ultimo_cerrado = datetime(2022, ultimo_mes_cerrado, 1).strftime('%B')
    nombre_mes_ultimo_cerrado_es = meses.get(nombre_mes_ultimo_cerrado)

    datos_ultimo_mes = company_data[(company_data['FECHA'].dt.month == ultimo_mes_cerrado) & (company_data['FECHA'].dt.year == año_ultimo_mes_cerrado)]
    if not datos_ultimo_mes.empty:
        max_cotizacion_mes = datos_ultimo_mes.loc[datos_ultimo_mes['PRECIO'].idxmax()]
        min_cotizacion_mes = datos_ultimo_mes.loc[datos_ultimo_mes['PRECIO'].idxmin()]
        max_quotes.append({'AÑO': f'{nombre_mes_ultimo_cerrado_es.capitalize()} {año_ultimo_mes_cerrado}', 'FECHA': format_date(max_cotizacion_mes['FECHA']), 'PRECIO': format_price(max_cotizacion_mes['PRECIO'])})
        min_quotes.append({'AÑO': f'{nombre_mes_ultimo_cerrado_es.capitalize()} {año_ultimo_mes_cerrado}', 'FECHA': format_date(min_cotizacion_mes['FECHA']), 'PRECIO': format_price(min_cotizacion_mes['PRECIO'])})

    return render_template('empresa.html', company=company, profile=profile, max_quotes=max_quotes, min_quotes=min_quotes, graph=graph, indices_financieros=indices_financieros, obtener_resumen_dividendos=obtener_resumen_dividendos)




@app.route('/renta-variable')
def renta_variable_view():
    # Leer los datos desde el archivo actualizado
    datos = pd.read_csv(datos_actualizados_path)
    # Limpiar y preparar los datos si es necesario
    datos = datos[datos['PRECIO_FINAL'].notnull()]

    hoy = datetime.now()
    fecha_actual = hoy.strftime('%d de %B de %Y')

    lunes_actual = hoy - timedelta(days=hoy.weekday())
    lunes_anterior = lunes_actual - timedelta(days=7)
    
    semana_actual_inicio = lunes_actual.strftime('%d de %B')
    semana_anterior_inicio = lunes_anterior.strftime('%d de %B')

    # Mapear los nombres de los meses en inglés a español
    meses = {
        'January': 'enero', 'February': 'febrero', 'March': 'marzo',
        'April': 'abril', 'May': 'mayo', 'June': 'junio',
        'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
        'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
    }

    for mes_ing, mes_esp in meses.items():
        semana_actual_inicio = semana_actual_inicio.replace(mes_ing, mes_esp)
        semana_anterior_inicio = semana_anterior_inicio.replace(mes_ing, mes_esp)
        fecha_actual = fecha_actual.replace(mes_ing, mes_esp)

    return render_template('renta_variable.html', datos=datos.to_dict(orient='records'), semana_actual_inicio=semana_actual_inicio, semana_anterior_inicio=semana_anterior_inicio, fecha_actual=fecha_actual)

@app.route('/data/<path:filename>')
def serve_data_file(filename):
    return send_from_directory('data', filename)

@app.route('/noticias')
def noticias():
    return render_template('noticias.html')

@app.route('/renta-fija')
def renta_fija():
    return render_template('renta_fija.html')

@app.route('/update-data') 
def update_data(): 
    os.system('python update_data.py') 
    os.system('python combine_data.py') 
    os.system('python actualizar_variacion.py') 
    return "Data updated successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
