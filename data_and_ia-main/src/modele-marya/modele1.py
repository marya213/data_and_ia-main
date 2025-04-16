import pandas as pd # type: ignore
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np

# === 1. Charger et préparer les données ===
def charger_et_preparer_donnees(temp_csv, conso_csv,
                                colonne_date="Date", colonne_temp="Temperature", colonne_conso="Consommation",
                                date_debut="2022-01-01", date_fin="2022-09-30"):
    # Charger température
    df_temp = pd.read_csv(temp_csv, usecols=[colonne_date, colonne_temp])
    df_temp[colonne_date] = pd.to_datetime(df_temp[colonne_date], utc=True)
    df_temp = df_temp[(df_temp[colonne_date] >= date_debut) & (df_temp[colonne_date] < date_fin)]
    df_temp[colonne_temp] = df_temp[colonne_temp] - 273.15  # Kelvin -> Celsius
    df_temp.set_index(colonne_date, inplace=True)
    df_temp.sort_index(inplace=True)

    # Charger consommation
    df_conso = pd.read_csv(conso_csv, usecols=[colonne_date, colonne_conso], sep=",", on_bad_lines="skip")
    df_conso[colonne_date] = pd.to_datetime(df_conso[colonne_date], utc=True, errors="coerce")
    df_conso.dropna(subset=[colonne_date, colonne_conso], inplace=True)
    df_conso[colonne_conso] = pd.to_numeric(df_conso[colonne_conso], errors="coerce")
    df_conso.dropna(subset=[colonne_conso], inplace=True)
    df_conso = df_conso[(df_conso[colonne_date] >= date_debut) & (df_conso[colonne_date] < date_fin)]
    df_conso.set_index(colonne_date, inplace=True)
    df_conso.sort_index(inplace=True)

    # Fusion fine (alignement temporel précis)
    df_merged = pd.merge_asof(
        df_conso, df_temp,
        left_index=True, right_index=True,
        direction='nearest',
        tolerance=pd.Timedelta("30min")  # ou autre selon la fréquence des mesures
    ).dropna()

    df_merged.rename(columns={colonne_temp: "Temp_Moy", colonne_conso: "Conso_Moy"}, inplace=True)

    return df_merged

# === 2. Créer et entraîner le modèle ===
def entrainer_modele(df):
    X = df[["Temp_Moy"]]
    y = df["Conso_Moy"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modele = LinearRegression()
    modele.fit(X_train, y_train)
    y_pred = modele.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\n📊 Évaluation du modèle :")
    print(f"➡️ R² : {r2:.2f}")
    print(f"➡️ RMSE : {rmse:.2f} kWh")

    return y_test, y_pred

# === 3. Visualisation ===
def afficher_resultats(y_test, y_pred):
    # Scatter Réel vs Prédit
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.7, edgecolors="k", color="blue")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Idéal : y = x")
    plt.xlabel("Consommation réelle (kWh)")
    plt.ylabel("Consommation prédite (kWh)")
    plt.title("Réel vs Prédit")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === 4. Pipeline complet ===
def pipeline():
    df = charger_et_preparer_donnees(
        temp_csv="donne_meteorologique.csv",
        conso_csv="Power.csv",
        date_debut="2022-01-01",
        date_fin="2022-09-25"
    )

    y_test, y_pred = entrainer_modele(df)
    afficher_resultats(y_test, y_pred)

# === Lancer l’analyse ===
pipeline()