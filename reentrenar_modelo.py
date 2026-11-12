import os
import pickle
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
import pandas as pd


DATA = Path(__file__).resolve().parent / "data"
CSV = DATA / "notas_credito_operaciones.csv"
PKL = DATA / "Modelo_NC.pkl"


class CotizadorNC:
    def __init__(self, operaciones):
        fechas = sorted(operaciones["fecha"].unique(), reverse=True)[:5]
        self.ultima_fecha = pd.Timestamp(fechas[0]).date()
        self.jornadas = []

        for fecha in fechas:
            filas = operaciones.loc[operaciones["fecha"] == fecha]
            montos = filas["valor_nominal"].to_numpy(dtype=float)
            precios = filas["precio"].to_numpy(dtype=float)
            self.jornadas.append((np.log(montos), precios))

    def estimar(self, nominal):
        if not np.isfinite(nominal) or nominal <= 0:
            raise ValueError("El valor nominal debe ser positivo y finito.")

        objetivo = np.log(nominal)
        limite_distancia = np.log(1.5)
        cercanas = []
        disponibles = []

        for antiguedad, (montos_log, precios) in enumerate(self.jornadas):
            distancias = np.abs(montos_log - objetivo)
            indices = np.argsort(distancias, kind="stable")[:5]

            for indice in indices:
                distancia = float(distancias[indice])
                operacion = (distancia, antiguedad, float(precios[indice]))
                disponibles.append(operacion)

                if distancia <= limite_distancia:
                    cercanas.append(operacion)

            if len(cercanas) >= 3:
                break

        seleccion = cercanas[:5]

        if not seleccion:
            disponibles.sort(key=lambda fila: (fila[0], fila[1]))
            seleccion = disponibles[:5]

        distancias, jornadas_atras, precios = np.asarray(seleccion).T
        pesos = np.exp(-distancias) / (1 + jornadas_atras)
        return float(np.average(precios, weights=pesos))

    def predict(self, X):
        valores = np.asarray(X, dtype=float)
        if valores.ndim != 2 or valores.shape[1] != 1:
            raise ValueError("Se espera una columna con el valor nominal.")

        return np.array([self.estimar(monto) for monto in valores[:, 0]])


def reentrenar():
    columnas = ["fecha", "titulo", "valor_nominal", "precio"]
    datos = pd.read_csv(CSV, sep=";", usecols=columnas)

    ordinarias = datos["titulo"].str.strip().str.upper().eq("NOTAS DE CREDITO")
    datos = datos.loc[ordinarias].copy()

    if datos.empty:
        raise ValueError("El CSV no contiene notas de crédito ordinarias.")

    datos["fecha"] = pd.to_datetime(
        datos["fecha"], format="ISO8601", errors="raise"
    ).dt.normalize()

    montos = datos[["valor_nominal", "precio"]].apply(pd.to_numeric, errors="raise")
    if (
        datos["fecha"].isna().any()
        or not np.isfinite(montos).all().all()
        or (montos <= 0).any().any()
    ):
        raise ValueError("Hay fechas, nominales o precios inválidos en el CSV.")

    datos[["valor_nominal", "precio"]] = montos
    modelo = CotizadorNC(datos)

    with NamedTemporaryFile(dir=DATA, suffix=".tmp", delete=False) as archivo:
        temporal = Path(archivo.name)

    try:
        with temporal.open("wb") as archivo:
            pickle.dump(modelo, archivo, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(temporal, PKL)
    finally:
        temporal.unlink(missing_ok=True)

    print(f"Modelo guardado: {PKL.name} | Última jornada: {modelo.ultima_fecha}")


if __name__ == "__main__":
    # Flask podrá localizar la clase al cargar el modelo guardado.
    from reentrenar_modelo import reentrenar as ejecutar

    ejecutar()