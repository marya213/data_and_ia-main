from sklearn.ensemble import RandomForestRegressor


# === Import des bibliothèques nécessaires ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score   

# === Import des modules de l'application ===
from src.app.methode.clear_content import clear_content 




def view_model_3(frame):
    """
    Affiche un modèle Random Forest (modèle plus avancé) dans l'interface Tkinter.

    Args:
        frame (tk.Frame): Le conteneur Tkinter où le modèle sera affiché.
    """
    # Nettoyer l'interface
    clear_content(frame)

    try:
        # Charger les données enrichies
        df = load_data_rf()

        # === Préparation des données ===
        X = df[["Temp_Moy", "Temp_Moy_3j", "Jour_semaine", "Mois", "Conso_Lag1"]]
        y = df["Conso_Moy"]

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Modèle Random Forest
        modele = RandomForestRegressor(n_estimators=100, random_state=42)
        modele.fit(X_train, y_train)
        y_pred = modele.predict(X_test)

        # Métriques
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Affichage des scores
        perf_label = ttk.Label(
            frame,
            text=f"Modèle Random Forest\nR² = {r2:.2f} | RMSE = {rmse:.2f} kWh",
            font=("Arial", 12, "bold")
        )
        perf_label.pack(pady=10)

        # Graphique
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(y_test, y_pred, alpha=0.7, edgecolors="k", color="green")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
        ax.set_xlabel("Consommation réelle (kWh)")
        ax.set_ylabel("Consommation prédite (kWh)")
        ax.set_title("Réel vs Prédit (Random Forest)")
        ax.grid(True)

        # Affichage dans Tkinter
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Erreur", f"Analyse RF échouée : {e}")


def load_data_rf():
    """
    Chargement + enrichissement des données pour modèle Random Forest.
    """
    df_temp = pd.read_csv("data/donne_meteorologique.csv", usecols=["Date", "Temperature"])
    df_temp["Date"] = pd.to_datetime(df_temp["Date"], utc=True)
    df_temp.set_index("Date", inplace=True)
    df_temp["Temperature"] = df_temp["Temperature"] - 273.15
    temp_journalier = df_temp["Temperature"].resample("D").mean().rename("Temp_Moy")

    df_conso = pd.read_csv("data/Power.csv", usecols=["Date", "Consommation"])
    df_conso["Date"] = pd.to_datetime(df_conso["Date"], utc=True, errors="coerce")
    df_conso["Consommation"] = pd.to_numeric(df_conso["Consommation"], errors="coerce")
    df_conso.set_index("Date", inplace=True)
    conso_journalier = df_conso["Consommation"].resample("D").mean().rename("Conso_Moy")

    df = pd.concat([temp_journalier, conso_journalier], axis=1).dropna()

    # Enrichissement
    df["Jour_semaine"] = df.index.dayofweek
    df["Mois"] = df.index.month
    df["Temp_Moy_3j"] = df["Temp_Moy"].rolling(window=3).mean()
    df["Conso_Lag1"] = df["Conso_Moy"].shift(1)
    df.dropna(inplace=True)

    return df
