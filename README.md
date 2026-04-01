# Software Defect Prediction System

Sistema de Machine Learning para predecir si un módulo de software contiene defectos, basado en métricas de código fuente. Utiliza **Regresión Logística** entrenada sobre el dataset público **JM1** (NASA Metrics Data Program).

---

##  ¿Qué problema resuelve?

Durante el desarrollo de software, detectar defectos antes de que lleguen a producción es costoso y difícil. Este sistema analiza métricas estáticas del código (como complejidad ciclomática, líneas de código, número de operadores, etc.) y predice automáticamente si un módulo tiene alta probabilidad de contener bugs.

---

##  ¿Cómo funciona el modelo?

1. **Preprocesamiento**: Se limpian los datos del dataset JM1, se eliminan valores nulos y se normalizan las variables numéricas con `StandardScaler`.
2. **Entrenamiento**: Se entrena un clasificador de **Regresión Logística** que aprende a distinguir módulos defectuosos de los que no lo son.
3. **Serialización**: El modelo entrenado y el escalador se guardan como archivos `.pkl` para ser reutilizados sin reentrenar.
4. **Predicción**: Dado un conjunto de métricas nuevas, el modelo retorna si el módulo es defectuoso o no, junto con la probabilidad asociada.
5. **Interfaz web**: Una aplicación Flask permite ingresar métricas manualmente y visualizar predicciones en tiempo real desde el navegador.
6. **Historial**: Cada predicción se registra en un archivo CSV para trazabilidad y auditoría.

---

##  Estructura del proyecto

```
project/
├── data/
│   ├── jm1.csv                    # Dataset original (ver sección Dataset)
│   └── predictions_log.csv        # Historial de predicciones (se genera automáticamente)
│
├── src/
│   ├── train.py                   # Script de entrenamiento del modelo
│   ├── predict.py                 # Script de predicción en consola
│   ├── features.py                # Definición y descripción de las variables de entrada
│   └── preprocessing.py           # Limpieza y transformación de datos
│
├── app/
│   ├── app.py                     # Servidor Flask (API + renderizado web)
│   └── templates/
│   │   ├── index.html             # Formulario de predicción
│   │   └── history.html           # Historial de predicciones
│   └── static/
│       └── style.css              # Estilos de la interfaz web
│
├── model/
│   ├── model.pkl                  # Modelo entrenado (se genera con train.py)
│   └── scaler.pkl                 # Escalador de características (se genera con train.py)
│
├── Dockerfile                     # Imagen Docker para despliegue
├── docker-compose.yml             # Orquestación de servicios con Docker Compose
├── requirements.txt               # Dependencias de Python
└── README.md
```

---

##  Requisitos

- Python **3.9 o superior**
- pip

Instalar dependencias:

```bash
pip install -r requirements.txt
```

> Las dependencias principales incluyen: `scikit-learn`, `pandas`, `numpy`, `flask`, `joblib`.

---

##  Dataset

El sistema utiliza el dataset **JM1** del programa NASA Metrics Data Program, que contiene métricas de código fuente de sistemas escritos en C.

### Variables de entrada (features)

| Variable | Descripción |
|----------|-------------|
| `loc` | Líneas de código |
| `v(g)` | Complejidad ciclomática de McCabe |
| `ev(g)` | Complejidad esencial |
| `iv(g)` | Complejidad de diseño |
| `n` | Longitud total de Halstead |
| `v` | Volumen de Halstead |
| `l` | Nivel de Halstead |
| `d` | Dificultad de Halstead |
| `i` | Inteligencia del programa |
| `e` | Esfuerzo de Halstead |
| `b` | Estimación de bugs (Halstead) |
| `t` | Tiempo de programación estimado |
| `lOCode` | Líneas de código real |
| `lOComment` | Líneas de comentario |
| `lOBlank` | Líneas en blanco |
| `lOCodeAndComment` | Líneas mixtas |
| `uniq_Op` | Operadores únicos |
| `uniq_Opnd` | Operandos únicos |
| `total_Op` | Total de operadores |
| `total_Opnd` | Total de operandos |
| `branchCount` | Número de ramas del código |

### Variable objetivo

| Variable | Descripción |
|----------|-------------|
| `defects` | `true` si el módulo tiene defectos, `false` si no |

### ¿Dónde colocar el archivo?

Descarga el dataset y colócalo en:

```
data/jm1.csv
```

> Puedes obtenerlo en: [Promise Repository](http://promise.site.uottawa.ca/SERepository/datasets-page.html) o en [OpenML - JM1](https://www.openml.org/d/1053)

---

##  Entrenamiento del modelo

Ejecuta el script de entrenamiento con:

```bash
python src/train.py
```

Este script:
1. Carga y limpia el dataset JM1
2. Separa los datos en entrenamiento (80%) y prueba (20%)
3. Normaliza las features con `StandardScaler`
4. Entrena el modelo de Regresión Logística
5. Evalúa el modelo (accuracy, precision, recall, F1-score)
6. Guarda los artefactos:
   - `model/model.pkl` — modelo entrenado
   - `model/scaler.pkl` — escalador ajustado

>  **Importante**: El modelo debe entrenarse antes de ejecutar la aplicación web o las predicciones por consola.

---

##  Predicción en consola

Para probar el modelo sin abrir la aplicación web, puedes ejecutar directamente:

```bash
python src/predict.py
```

El script toma un ejemplo de métricas predefinido, lo escala con `scaler.pkl` y genera una predicción con su probabilidad estimada.

---

##  Aplicación Web (Flask)

### Iniciar el servidor

```bash
python app/app.py
```

Abre tu navegador en:

```
http://127.0.0.1:5000/
```

### Rutas disponibles

| Ruta | Descripción |
|------|-------------|
| `/` | Formulario de predicción con todas las variables |
| `/predict` | Endpoint POST que devuelve el resultado |
| `/history` | Tabla con el historial completo de predicciones |

### Flujo de una predicción

1. El usuario ingresa las métricas del módulo en el formulario.
2. La aplicación escala los valores con `scaler.pkl`.
3. El modelo `model.pkl` realiza la predicción.
4. Se muestra el resultado: **Defectuoso / No defectuoso** con la probabilidad.
5. El resultado se registra automáticamente en `data/predictions_log.csv`.

---

##  Despliegue con Docker

Docker permite empaquetar la aplicación con todas sus dependencias en un contenedor portable. No necesitas instalar Python ni librerías en tu máquina local.

### Prerequisitos

- [Docker](https://docs.docker.com/get-docker/) instalado y corriendo
- [Docker Compose](https://docs.docker.com/compose/install/) (incluido en Docker Desktop)

### Archivos necesarios

**`Dockerfile`** — Define la imagen de la aplicación:

```dockerfile
# Imagen base con Python 3.11 liviano
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias primero (mejor uso de caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Asegurarse de que el modelo esté entrenado (opcional si ya existe)
# RUN python src/train.py

# Exponer el puerto de Flask
EXPOSE 5000

# Variables de entorno para Flask
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando de inicio
CMD ["python", "app/app.py"]
```

**`docker-compose.yml`** — Orquesta los servicios:

```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: defect-prediction-app
    ports:
      - "5000:5000"         # Puerto local:puerto del contenedor
    volumes:
      - ./data:/app/data    # Montar carpeta data para persistir predicciones y logs
      - ./model:/app/model  # Montar carpeta model para leer/escribir artefactos
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

### Construir y ejecutar

```bash
# Construir la imagen
docker build -t defect-prediction .

# Iniciar con Docker Compose (recomendado)
docker-compose up --build

# O sin Compose
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/model:/app/model \
  defect-prediction
```

La aplicación estará disponible en:

```
http://localhost:5000/
```

### Comandos útiles de Docker

```bash
# Ver contenedores activos
docker ps

# Detener la aplicación
docker-compose down

# Ver logs del contenedor
docker logs defect-prediction-app

# Entrar al contenedor (para depuración)
docker exec -it defect-prediction-app bash

# Reentrenar el modelo dentro del contenedor
docker exec defect-prediction-app python src/train.py
```

>  **Nota**: Los volúmenes (`volumes`) en `docker-compose.yml` permiten que el historial de predicciones y los modelos persistan aunque el contenedor se reinicie o se elimine.

---

##  Despliegue en AWS

AWS (Amazon Web Services) ofrece varias formas de desplegar esta aplicación. Las dos más comunes para proyectos de este tipo son **EC2** (máquina virtual) y **Elastic Beanstalk** (plataforma administrada).

---

### Opción A — AWS EC2 (recomendado para control total)

EC2 te da una máquina virtual en la nube donde puedes correr Docker tal como lo harías en local.

#### Paso 1: Crear la instancia

1. Ir a **AWS Console → EC2 → Launch Instance**
2. Elegir **Amazon Linux 2023** o **Ubuntu 22.04 LTS**
3. Seleccionar tipo de instancia: `t3.small` (mínimo recomendado para ML)
4. Crear o seleccionar un **Key Pair** (`.pem`) para acceso SSH
5. En **Security Group**, abrir los puertos:
   - `22` — SSH
   - `5000` — Flask (o `80` si usas Nginx como proxy)
6. Lanzar la instancia

#### Paso 2: Conectarse por SSH

```bash
chmod 400 tu-key.pem
ssh -i tu-key.pem ec2-user@<IP_PUBLICA_EC2>
```

#### Paso 3: Instalar Docker en la instancia

```bash
# Amazon Linux 2023
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -aG docker ec2-user

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar
docker --version
docker-compose --version
```

#### Paso 4: Clonar y desplegar

```bash
# Clonar tu repositorio
git clone https://github.com/tu-usuario/software-defect-prediction.git
cd software-defect-prediction

# Asegurarte de que el dataset está en data/jm1.csv
# (puedes subirlo con scp o descargarlo directamente)

# Entrenar el modelo
docker-compose run web python src/train.py

# Levantar la aplicación
docker-compose up -d
```

La aplicación estará disponible en:

```
http://<IP_PUBLICA_EC2>:5000/
```

---

## Notas

* El modelo es de clasificación (Logistic Regression)
* Se utiliza StandardScaler para normalización
* Los datos ingresados en la web no reentrenan el modelo automáticamente
* El reentrenamiento debe hacerse manualmente ejecutando train.py

---
