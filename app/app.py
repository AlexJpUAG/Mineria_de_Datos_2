from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

model = joblib.load("model/model.pkl")
scaler = joblib.load("model/scaler.pkl")

columns = [
    'loc','vg','evg','ivg','n','v','l','d','i','e','b','t',
    'lOCode','lOComment','lOBlank','locCodeAndComment',
    'uniq_Op','uniq_Opnd','total_Op','total_Opnd','branchCount'
]

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        try:
            data = [float(request.form[col]) for col in columns]

            df = pd.DataFrame([data], columns=columns)

            scaled = scaler.transform(df)
            pred = model.predict(scaled)[0]

            prediction = "TIENE defectos" if pred == 1 else "NO tiene defectos"

            # Guardar en CSV
            file_path = "data/predictions_log.csv"
            row = data + [int(pred)]
            columns_with_pred = columns + ["prediction"]

            df_log = pd.DataFrame([row], columns=columns_with_pred)

            if not os.path.exists(file_path):
                df_log.to_csv(file_path, index=False)
            else:
                df_log.to_csv(file_path, mode="a", header=False, index=False)

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template("index.html", columns=columns, prediction=prediction)


@app.route("/history")
def history():
    try:
        df = pd.read_csv("data/predictions_log.csv")
        data = df.to_dict(orient="records")
        return render_template("history.html", tables=data)
    except:
        return "No hay datos aún"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)