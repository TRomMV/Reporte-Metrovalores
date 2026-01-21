import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import pickle

# Ruta del archivo de datos
ruta_datos = r"C:\Users\tomas\Desktop\MetrovaloresApp\data\NC_semanal.csv"

# Cargar los datos con separador punto y coma
df = pd.read_csv(ruta_datos, sep=";")

# Verificar columnas disponibles
print("📄 Columnas detectadas:", df.columns.tolist())

# Validar tipos de datos
print("🔍 Tipos de datos:")
print(df[['valor_nominal', 'precio']].dtypes)

# Separar variables
X = df[['valor_nominal']]
y = df['precio']

# Entrenar el modelo KNN
modelo = KNeighborsRegressor(n_neighbors=33, weights='uniform')
modelo.fit(X, y)

# Guardar el modelo actualizado
ruta_modelo = r"C:\Users\tomas\Desktop\MetrovaloresApp\data\Modelo_NC.pkl"
with open(ruta_modelo, "wb") as f:
    pickle.dump(modelo, f)

print("✅ Modelo KNN actualizado y guardado en:", ruta_modelo)

# Prueba rápida de predicción
valores_prueba = [1000, 5000, 10000, 50000, 100000, 500000]
print("\n📊 Predicciones de prueba:")
for valor in valores_prueba:
    pred = modelo.predict([[valor]])[0]
    print(f"Valor nominal: {valor:,.2f} → Precio estimado: {pred:.4f}")
