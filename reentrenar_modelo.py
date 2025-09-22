import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Ruta completa del archivo de datos
ruta_datos = r"C:\Users\tomas\Desktop\MetrovaloresApp\data\NC_semanal.csv"

# Cargar los datos con separador punto y coma
df = pd.read_csv(ruta_datos, sep=";")

# Verificar columnas disponibles
print("Columnas detectadas:", df.columns.tolist())

# Separar variables
X = df[['valor_nominal']]
y = df['precio']

# Entrenar el modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Guardar el modelo actualizado en la misma carpeta
ruta_modelo = r"C:\Users\tomas\Desktop\MetrovaloresApp\data\Modelo_NC.pkl"
with open(ruta_modelo, "wb") as f:
    pickle.dump(modelo, f)

print("✅ Modelo actualizado y guardado en:", ruta_modelo)
