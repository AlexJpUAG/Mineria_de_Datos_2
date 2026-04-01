import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from features import get_features_and_target
import joblib

# 1. Cargar datos
df = pd.read_csv("data/jm1.csv")

# 2. Convertir columnas problemáticas a numéricas
cols_to_convert = ["uniq_Op", "uniq_Opnd", "total_Op", "total_Opnd", "branchCount"]

for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 3. Eliminar valores nulos
df = df.dropna()

# 4. Limpiar nombres de columnas
df.columns = df.columns.str.replace("(", "", regex=False)\
                       .str.replace(")", "", regex=False)\
                       .str.replace(" ", "_", regex=False)

# 5. Separar variables (usando features.py)
X, y = get_features_and_target(df)

# 6. Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Escalar datos
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 8. Entrenar modelo
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

# 9. Evaluar modelo
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy)
print("Confusion Matrix:")
print(cm)

# 10. Guardar modelo y scaler
joblib.dump(model, "model/model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("Modelo y scaler guardados en model/")