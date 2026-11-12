import os
import sys
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
import requests


URL = (
    "https://www.bolsadequito.com/uploads/estadisticas/"
    "boletines/cotizaciones-historicas/notas-credito.xls"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

SALIDA = Path(__file__).resolve().parent / "data" / "notas_credito_operaciones.csv"

COLUMNAS = {
    "FECHA": "fecha",
    "EMISOR": "emisor",
    "TITULO": "titulo",
    "PRECIO %": "precio",
    "VALOR NOMINAL (USD)": "valor_nominal",
    "VALOR EFECTIVO (USD)": "valor_efectivo",
    "PROCEDENCIA": "procedencia",
}


def actualizar_notas_credito(archivo_local=None):
    if archivo_local:
        contenido = Path(archivo_local).read_bytes()
    else:
        respuesta = requests.get(URL, headers=HEADERS, timeout=60)
        respuesta.raise_for_status()
        contenido = respuesta.content

    hojas = []
    with pd.ExcelFile(BytesIO(contenido), engine="xlrd") as libro:
        for nombre in libro.sheet_names:
            if not (nombre.isdigit() and len(nombre) == 4):
                continue

            # En el reporte de la BVQ, la fila 8 contiene los encabezados.
            datos = libro.parse(nombre, header=7, usecols=list(COLUMNAS))
            datos = datos.rename(columns=COLUMNAS)

            # Las notas al pie de la hoja no tienen título de negociación.
            datos = datos.dropna(subset=["titulo"]).copy()
            if datos.empty:
                continue

            datos["fecha"] = pd.to_datetime(datos["fecha"], errors="raise")
            for columna in ["valor_nominal", "precio", "valor_efectivo"]:
                datos[columna] = pd.to_numeric(datos[columna], errors="raise")

            obligatorias = ["fecha", "valor_nominal", "precio"]
            if datos[obligatorias].isna().any().any():
                raise ValueError(f"Hay operaciones incompletas en la hoja {nombre}.")

            hojas.append(datos)

    if not hojas:
        raise ValueError("El Excel de la BVQ no contiene operaciones en hojas anuales.")

    operaciones = pd.concat(hojas, ignore_index=True)
    operaciones = operaciones.sort_values("fecha", kind="stable")
    ultima_fecha = operaciones["fecha"].max().date()

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    if SALIDA.exists():
        anterior = pd.read_csv(SALIDA, sep=";", usecols=["fecha"])
        if not anterior.empty:
            ultima_guardada = pd.to_datetime(anterior["fecha"]).max().date()
            if ultima_fecha < ultima_guardada:
                raise ValueError(
                    f"El Excel llega al {ultima_fecha}, pero el CSV guardado "
                    f"ya contiene operaciones hasta el {ultima_guardada}."
                )

    # Reemplazar el CSV solo después de terminar de escribir todas las filas.
    with NamedTemporaryFile(dir=SALIDA.parent, suffix=".tmp", delete=False) as tmp:
        temporal = Path(tmp.name)

    try:
        operaciones.to_csv(temporal, sep=";", index=False, date_format="%Y-%m-%d")
        os.replace(temporal, SALIDA)
    finally:
        temporal.unlink(missing_ok=True)

    return len(operaciones), ultima_fecha


if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else None
    total, fecha = actualizar_notas_credito(archivo)
    print(
        f"{total} operaciones | Última negociación: {fecha} | "
        f"Archivo: {SALIDA.name}"
    )