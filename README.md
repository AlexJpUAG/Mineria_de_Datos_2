```md
# Software Defect Prediction System

Este proyecto implementa un sistema completo de Machine Learning para la predicción de defectos en software utilizando un modelo de clasificación.

## Descripción

El sistema permite:
- Entrenar un modelo de Machine Learning
- Realizar predicciones en local
- Exponer el modelo mediante una aplicación web con Flask
- Guardar un historial de predicciones

---

## Estructura del proyecto

```

project/

data/
jm1.csv
predictions_log.csv (se genera automáticamente)

src/
train.py
predict.py
features.py
preprocessing.py

app/
app.py
templates/
index.html
history.html
static/
style.css

model/
model.pkl
scaler.pkl

requirements.txt
README.md

````

---

## Requisitos

- Python 3.9 o superior

Instalar dependencias:

```bash
pip install -r requirements.txt
````

---

## Dataset

El proyecto utiliza el dataset JM1 de predicción de defectos de software.

Debe colocarse en:

```
data/jm1.csv
```

---

## Entrenamiento del modelo

Para entrenar el modelo:

```bash
python src/train.py
```

Esto generará:

* model/model.pkl
* model/scaler.pkl

---

## Predicción en local

Para probar el modelo sin la aplicación web:

```bash
python src/predict.py
```

---

## Ejecutar la aplicación web

Para iniciar la aplicación Flask:

```bash
python app/app.py
```

Abrir en navegador:

```
http://127.0.0.1:5000/
```

---

## Funcionalidades de la aplicación

### Página principal

* Formulario para ingresar variables
* Predicción en tiempo real

### Historial

* URL: /history
* Muestra todas las predicciones realizadas
* Los datos se almacenan en:

```
data/predictions_log.csv
```

---

## Notas

* El modelo es de clasificación (Logistic Regression)
* Se utiliza StandardScaler para normalización
* Los datos ingresados en la web no reentrenan el modelo automáticamente
* El reentrenamiento debe hacerse manualmente ejecutando train.py

---
