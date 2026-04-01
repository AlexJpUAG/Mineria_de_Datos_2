import pandas as pd

def clean_data(df):
    # Convertir columnas a numéricas
    cols_to_convert = ["uniq_Op", "uniq_Opnd", "total_Op", "total_Opnd", "branchCount"]

    for col in cols_to_convert:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Eliminar valores nulos
    df = df.dropna()

    # Limpiar nombres de columnas
    df.columns = df.columns.str.replace("(", "", regex=False)\
                           .str.replace(")", "", regex=False)\
                           .str.replace(" ", "_", regex=False)

    return df