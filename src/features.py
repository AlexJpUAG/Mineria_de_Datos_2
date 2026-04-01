def get_features_and_target(df):
    X = df.drop("defects", axis=1)
    y = df["defects"].astype(int)

    return X, y