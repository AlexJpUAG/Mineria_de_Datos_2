import pandas as pd
import joblib

# 1. Cargar modelo y scaler
model = joblib.load("model/model.pkl")
scaler = joblib.load("model/scaler.pkl")

# 2. Crear datos de prueba (ejemplo manual)
# IMPORTANTE: deben tener el mismo orden de columnas que el entrenamiento

sample_data = [[
    50,   # loc
    5,    # vg
    1,    # evg
    4,    # ivg
    150,  # n
    800,  # v
    0.05, # l
    10,   # d
    30,   # i
    4000, # e
    0.1,  # b
    200,  # t
    40,   # lOCode
    5,    # lOComment
    2,    # lOBlank
    45,   # locCodeAndComment
    10,   # uniq_Op
    20,   # uniq_Opnd
    60,   # total_Op
    40,   # total_Opnd
    8     # branchCount
]]

# 3. Convertir a DataFrame (opcional pero recomendable)
columns = [
    'loc','vg','evg','ivg','n','v','l','d','i','e','b','t',
    'lOCode','lOComment','lOBlank','locCodeAndComment',
    'uniq_Op','uniq_Opnd','total_Op','total_Opnd','branchCount'
]

df = pd.DataFrame(sample_data, columns=columns)

# 4. Escalar datos
scaled_data = scaler.transform(df)

# 5. Predecir
prediction = model.predict(scaled_data)

# 6. Mostrar resultado
print("Predicción:", prediction[0])

if prediction[0] == 1:
    print("El módulo TIENE defectos")
else:
    print("El módulo NO tiene defectos")