````md
# Sistema de Predicción de Defectos en Software

## 1. Introducción

El presente proyecto tiene como objetivo el desarrollo de un sistema completo de Machine Learning capaz de predecir defectos en módulos de software a partir de métricas estáticas del código.

El sistema implementa un flujo end-to-end que incluye:
- Carga de datos
- Preprocesamiento
- Entrenamiento de modelo
- Evaluación
- Serialización
- Implementación en una aplicación web con Flask

---

## 2. Descripción del Problema

Se aborda un problema de **clasificación supervisada**, donde el objetivo es determinar si un módulo de software presenta defectos (`defects = true/false`).

Aunque el enunciado menciona regresión, el dataset seleccionado corresponde naturalmente a un problema de clasificación, ya que la variable objetivo es categórica.

---

## 3. Dataset

Se utilizó el dataset:

Software Defect Prediction Dataset  
https://www.kaggle.com/datasets/semustafacevik/software-defect-prediction

Características principales:
- 10,885 instancias
- 22 atributos
- Variables numéricas basadas en métricas de código (McCabe y Halstead)
- Variable objetivo: `defects` (booleano)

---

## 4. Preprocesamiento de Datos

El preprocesamiento se implementa directamente en `train.py` y de forma modular en `preprocessing.py`.

### Acciones realizadas:

1. Conversión de columnas a tipo numérico:
```python
cols_to_convert = ["uniq_Op", "uniq_Opnd", "total_Op", "total_Opnd", "branchCount"]

for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors="coerce")
````

2. Eliminación de valores nulos:

```python
df = df.dropna()
```

3. Limpieza de nombres de columnas:

```python
df.columns = df.columns.str.replace("(", "", regex=False)\
                       .str.replace(")", "", regex=False)\
                       .str.replace(" ", "_", regex=False)
```

Estas transformaciones aseguran que los datos sean consistentes y compatibles con el modelo.

---

## 5. Feature Engineering

Se implementó el archivo `features.py` para separar variables independientes y dependiente:

```python
def get_features_and_target(df):
    X = df.drop("defects", axis=1)
    y = df["defects"].astype(int)
    return X, y
```

Esto permite modularidad y reutilización del código.

---

## 6. Entrenamiento del Modelo

El entrenamiento se realiza en `train.py`.

### División de datos:

```python
train_test_split(X, y, test_size=0.2, random_state=42)
```

Se utilizó una división 80/20.

---

### Escalamiento de datos

Se utilizó `StandardScaler`:

```python
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

#### Justificación:

El modelo utilizado (Regresión Logística) es sensible a la escala de los datos, por lo que el escalamiento mejora la convergencia y el rendimiento.

---

### Modelo utilizado

```python
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)
```

#### Justificación:

* Adecuado para problemas de clasificación binaria
* Interpretabilidad
* Buen desempeño con datos numéricos

---

## 7. Evaluación del Modelo

### Métrica utilizada:

* Accuracy
* Matriz de confusión

### Resultados obtenidos:

```
Accuracy: 0.8120404411764706
```

Matriz de confusión:

```
[[1716   41]
 [ 368   51]]
```

### Interpretación:

* El modelo clasifica correctamente la mayoría de los casos negativos (sin defectos)
* Existe un número considerable de falsos negativos (defectos no detectados)
* El dataset está desbalanceado, lo cual impacta el desempeño

---

## 8. Serialización del Modelo

Se utilizó `joblib` para guardar el modelo y el scaler:

```python
joblib.dump(model, "model/model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
```

Esto permite reutilizar el modelo sin necesidad de reentrenar.

---

## 9. Predicción Local

Archivo: `predict.py`

Permite probar el modelo con datos manuales:

```python
scaled_data = scaler.transform(df)
prediction = model.predict(scaled_data)
```

Esto valida el correcto funcionamiento del modelo antes de integrarlo en la aplicación web.

---

## 10. Aplicación Web con Flask

Archivo: `app.py`

### Funcionalidades:

* Carga del modelo al iniciar:

```python
model = joblib.load("model/model.pkl")
scaler = joblib.load("model/scaler.pkl")
```

* Recepción de datos desde formulario web
* Transformación y predicción
* Visualización del resultado

---

### Endpoint principal:

Ruta `/`

Permite:

* Ingresar datos manualmente
* Obtener predicción en tiempo real

---

### Almacenamiento de predicciones

Las predicciones se guardan en:

```
data/predictions_log.csv
```

Código:

```python
df_log.to_csv(file_path, mode="a", header=False, index=False)
```

---

### Historial

Ruta `/history`

Permite visualizar todas las predicciones realizadas en formato tabular.

---

## 11. Arquitectura del Proyecto

```
project/

data/
    jm1.csv
    predictions_log.csv

src/
    preprocessing.py
    features.py
    train.py
    predict.py

app/
    app.py
    templates/
    static/

model/
    model.pkl
    scaler.pkl
```

---

## 12. Consideraciones y Limitaciones

* El modelo no se reentrena automáticamente con nuevos datos
* El dataset presenta desbalance de clases
* No se implementaron métricas adicionales como recall o precision
* No se implementó pipeline de CI/CD ni despliegue en AWS (pendiente)

---

## 13. Conclusiones

Se logró construir un sistema funcional de Machine Learning que:

* Entrena un modelo de clasificación
* Realiza predicciones en tiempo real
* Expone el modelo mediante una aplicación web
* Almacena resultados para análisis posterior

El sistema cumple con los requerimientos fundamentales del proyecto y sienta las bases para futuras mejoras como:

* Balanceo de datos
* Mejora de métricas
* Despliegue en la nube
* Automatización del entrenamiento

```
```
