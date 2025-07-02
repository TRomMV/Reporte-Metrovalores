from flask import Flask, render_template, request, send_from_directory
import pickle
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



model = pickle.load(open("data/Modelo_NC.pkl", "rb"))


# Ruta de los archivos CSV
datos_actualizados_path = 'data/datos_actualizados.csv'
acciones_combinadas_path = 'data/acciones_combinadas.csv'  # Archivo de datos de empresas
rendimiento_sector_financiero_path = pd.read_csv('data/rendimiento_sector_financiero.csv')
rendimiento_sector_real_path = pd.read_csv('data/rendimiento_bolsas.csv')
rendimiento_bolsas_path = pd.read_csv('data/rendimiento_sector_real.csv')


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

# Definir las rutas a los archivos de datos
rendimiento_sector_financiero_path = 'data/rendimiento_sector_financiero.csv'
rendimiento_bolsas_path = 'data/rendimiento_bolsas.csv'
rendimiento_sector_real_path = 'data/rendimiento_sector_real.csv'

# Leer los datos de los archivos de rendimiento
df_financiero = pd.read_csv(rendimiento_sector_financiero_path)
df_bolsas = pd.read_csv(rendimiento_bolsas_path)
df_real = pd.read_csv(rendimiento_sector_real_path)

# Convertir la columna 'RENDIMIENTO' a valores numéricos (eliminar el símbolo % y convertir a flotante)
df_financiero.columns = df_financiero.columns.str.strip().str.upper()  # Normalizar las columnas a mayúsculas
df_bolsas.columns = df_bolsas.columns.str.strip().str.upper()  # Normalizar las columnas a mayúsculas
df_real.columns = df_real.columns.str.strip().str.upper()  # Normalizar las columnas a mayúsculas

# Verificar que las columnas requeridas existan en cada DataFrame
required_columns = ['AÑO', 'EMISOR', 'RENDIMIENTO']

for df_name, df in [('Financiero', df_financiero), ('Bolsas', df_bolsas), ('Real', df_real)]:
    if not all(column in df.columns for column in required_columns):
        raise KeyError(f"Las columnas 'AÑO', 'EMISOR' o 'RENDIMIENTO' no se encuentran en los datos de {df_name}. Verifique que los datos estén en el formato correcto.")

# Limpiar y convertir la columna 'RENDIMIENTO' a valores numéricos
df_financiero['RENDIMIENTO'] = df_financiero['RENDIMIENTO'].str.replace('%', '', regex=False).astype(float) / 100
df_bolsas['RENDIMIENTO'] = df_bolsas['RENDIMIENTO'].str.replace('%', '', regex=False).astype(float) / 100
df_real['RENDIMIENTO'] = df_real['RENDIMIENTO'].str.replace('%', '', regex=False).astype(float) / 100

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
    fecha_inicio_auto = datetime(2020, 1, 1)
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
    años = list(range(2020, 2025))
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

    # Mapeo de los meses en inglés a español
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

    # Renderizar el template con los datos necesarios
    return render_template(
        'renta_variable.html',
        datos=datos.to_dict(orient='records'),
        semana_actual_inicio=semana_actual_inicio,
        semana_anterior_inicio=semana_anterior_inicio,
        fecha_actual=fecha_actual
    )
colores = {
    'BANCO PICHINCHA C.A.': '#F7B600',
    'BANCO BOLIVARIANO C.A.': '#004B87',
    'BANCO GUAYAQUIL S.A.': '#E12D84',
    'BANCO DE LA PRODUCCION S.A . PRODUBANCO': '#006B3F',
    'HOLCIM ECUADOR S.A.': '#0072C6',
    'SAN CARLOS SOC. AGR. IND.': '#006B3F',
    'CERVECERIA NACIONAL CN S A': '#E12D39',
    'BEVERAGE BRAND PATENTS SA': '#9E9E9E',
    'BOLSA DE VALORES DE QUITO': '#E12D2D',
    'BOLSA DE VALORES DE GUAYAQUIL': '#6EC2E8'
}

@app.route('/grafico-tres-empresas')
def grafico_tres_empresas():
    empresas = ['BANCO PICHINCHA C.A.', 'BANCO BOLIVARIANO C.A.', 'BANCO GUAYAQUIL S.A.', 'BANCO DE LA PRODUCCION S.A . PRODUBANCO']
    fig = go.Figure()

    for empresa in empresas:
        datos_empresa = df_financiero[df_financiero['EMISOR'] == empresa]
        fig.add_trace(go.Scatter(
            x=datos_empresa['AÑO'],
            y=datos_empresa['RENDIMIENTO'],
            mode='lines+markers',
            name=empresa,
            line=dict(color=colores[empresa])
        ))

    fig.update_layout(
        title='Tendencias de Rendimiento: Pichincha, Bolivariano y Guayaquil',
        xaxis_title='Año',
        yaxis_title='Rendimiento (%)',
        hovermode='x unified',
        legend=dict(x=0, y=1.2),
        xaxis=dict(
            tickmode='array',
            tickvals=[2020, 2021, 2022, 2023, 2024],
            ticktext=['2020', '2021', '2022', '2023', '2024']
        ),
        yaxis=dict(tickformat=".1%")
    )

    config = dict(
        scrollZoom=True,
        displayModeBar=True,
        modeBarButtonsToRemove=['zoom2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d'],
        displaylogo=False
    )

    return fig.to_html(full_html=False, config=config)

@app.route('/grafico-bolsas')
def grafico_bolsas():
    empresas = ['BOLSA DE VALORES DE QUITO', 'BOLSA DE VALORES DE GUAYAQUIL']
    fig = go.Figure()

    for empresa in empresas:
        datos_empresa = df_bolsas[df_bolsas['EMISOR'] == empresa]
        fig.add_trace(go.Scatter(
            x=datos_empresa['AÑO'],
            y=datos_empresa['RENDIMIENTO'],
            mode='lines+markers',
            name=empresa,
            line=dict(color=colores[empresa])
        ))

    fig.update_layout(
        title='Tendencias de Rendimiento: Bolsas de Quito y Guayaquil',
        xaxis_title='Año',
        yaxis_title='Rendimiento (%)',
        hovermode='x unified',
        legend=dict(x=0, y=1.2),
        xaxis=dict(
            tickmode='array',
            tickvals=[2020, 2021, 2022, 2023, 2024],
            ticktext=['2020', '2021', '2022', '2023', '2024']
        ),
        yaxis=dict(tickformat=".1%")
    )

    config = dict(
        scrollZoom=True,
        displayModeBar=True,
        modeBarButtonsToRemove=['zoom2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d'],
        displaylogo=False
    )

    return fig.to_html(full_html=False, config=config)


@app.route('/grafico-sector-real')
def grafico_sector_real():
    empresas = [
        'HOLCIM ECUADOR S.A.', 
        'SAN CARLOS SOC. AGR. IND.', 
        'CERVECERIA NACIONAL CN S A', 
        'BEVERAGE BRAND PATENTS SA',
        'CORPORACION FAVORITA C.A.'  # Se incluye Corporación Favorita
    ]

    # Colores actualizados para cada empresa
    colores = {
        'HOLCIM ECUADOR S.A.': '#5BC0EB',  # Azul claro
        'SAN CARLOS SOC. AGR. IND.': '#00A859',  # Verde
        'CERVECERIA NACIONAL CN S A': '#FFD700',  # Amarillo
        'BEVERAGE BRAND PATENTS SA': '#A9A9A9',  # Gris
        'CORPORACION FAVORITA C.A.': '#FF0000'  # Rojo
    }

    fig = go.Figure()

    for empresa in empresas:
        datos_empresa = df_real[df_real['EMISOR'] == empresa]
        fig.add_trace(go.Scatter(
            x=datos_empresa['AÑO'],
            y=datos_empresa['RENDIMIENTO'],
            mode='lines+markers',
            name=empresa,
            line=dict(color=colores[empresa], width=2),
            marker=dict(color=colores[empresa], size=6)
        ))

    fig.update_layout(
        title='Tendencias de Rendimiento: Sector Real',
        xaxis_title='Año',
        yaxis_title='Rendimiento (%)',
        hovermode='x unified',
        legend=dict(x=0, y=1.2),
        xaxis=dict(
            tickmode='array',
            tickvals=[2020, 2021, 2022, 2023, 2024],
            ticktext=['2020', '2021', '2022', '2023', '2024']
        ),
        yaxis=dict(tickformat=".1%")
    )

    config = dict(
        scrollZoom=True,
        displayModeBar=True,
        modeBarButtonsToRemove=['zoom2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d'],
        displaylogo=False
    )

    return fig.to_html(full_html=False, config=config)



@app.route('/juntas-de-accionistas')
def juntas_de_accionistas():
    # Leer los datos desde el archivo combinado
    df_empresas = pd.read_csv(acciones_combinadas_path)

    df_empresas.columns = df_empresas.columns.str.strip().str.upper()
    if 'FECHA' not in df_empresas.columns or 'EMISOR' not in df_empresas.columns or 'VALOR' not in df_empresas.columns:
        raise KeyError("Las columnas necesarias no existen en los datos.")

    df_empresas['FECHA'] = pd.to_datetime(df_empresas['FECHA'], errors='coerce')
    df_empresas = df_empresas.dropna(subset=['FECHA'])

    df_empresas = df_empresas[(df_empresas['PRECIO'].notnull()) & (df_empresas['VALOR'] == 'ACCIONES')]

    # Leer los datos de rendimiento para el sector financiero
    df_rendimiento = pd.read_csv(rendimiento_sector_financiero_path)
    df_rendimiento.columns = df_rendimiento.columns.str.strip().str.upper()
    df_rendimiento['RENDIMIENTO'] = df_rendimiento['RENDIMIENTO'].str.replace('%', '', regex=False).astype(float) / 100

    # Generar los gráficos para cada sector
    grafico_tres_empresas_html = grafico_tres_empresas()
    grafico_bolsas_html = grafico_bolsas()
    grafico_sector_real_html = grafico_sector_real()

    # Renderizar el template de Juntas de Accionistas
    return render_template(
        'juntas_de_accionistas.html',
        grafico_tres_empresas=grafico_tres_empresas_html,
        grafico_bolsas=grafico_bolsas_html,
        grafico_sector_real=grafico_sector_real_html
    )



@app.route('/data/<path:filename>')
def serve_data_file(filename):
    return send_from_directory('data', filename)

@app.route("/notas-de-credito")
def notas_de_credito():
    return render_template("notas_de_credito.html")  # Asegúrate de que el archivo HTML está en la carpeta `templates`

@app.route("/predict", methods=["POST"])
def predict():
    valor_nominal = float(request.form["Valor_Nominal"])
    prediction = model.predict([[valor_nominal]])[0]
    prediction_text = f"El precio estimado para una nota de crédito con valor nominal de ${valor_nominal:,.2f} es: {prediction:,.2f}"
    return render_template("notas_de_credito.html", prediction_text=prediction_text)


@app.route('/update-data') 
def update_data(): 
    os.system('python update_data.py') 
    os.system('python combine_data.py') 
    os.system('python actualizar_variacion.py') 
    return "Data updated successfully!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
