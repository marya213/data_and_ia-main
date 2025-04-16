import pandas as pd
import matplotlib.pyplot as plt

def Moyen_Consommation(input_file, colonne):
    df = pd.read_csv(input_file, encoding='ISO-8859-1', index_col=0, header=0)
    df[colonne] = df[colonne].str.replace(',', '.').astype(float)
    return df[colonne].mean()

def Total_Consommation(input_file, colonne):
    df = pd.read_csv(input_file, encoding='ISO-8859-1', index_col=0, header=0)
    df[colonne] = df[colonne].str.replace(',', '.').astype(float)
    return df[colonne].sum()

def Consommation_Par_Habitant(input_file):
    df = pd.read_csv(input_file, encoding='ISO-8859-1', index_col=0, header=0)
    df['Conso totale (MWh)'] = df['Conso totale (MWh)'].str.replace(',', '.').astype(float)
    df['Nombre dhabitants'] = pd.to_numeric(df['Nombre dhabitants'].str.replace(',', '.'), errors='coerce')
    df = df.dropna(subset=['Nombre dhabitants'])
    df['Conso par habitant (MWh)'] = df['Conso totale (MWh)'] / df['Nombre dhabitants']
    moyenne_par_habitant = df['Conso par habitant (MWh)'].mean()
    total_par_habitant = df['Conso par habitant (MWh)'].sum()
    return moyenne_par_habitant, total_par_habitant


    

def Graphique_Consommation_Mensuelle(input_file):
    # Lecture du fichier CSV
    df = pd.read_csv(input_file, encoding='ISO-8859-1', header=0)
    
    try:
        # Conversion de la colonne 'Date' en format datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)
        df['mois'] = df['Date'].dt.month  # Extraction du mois
        
        # Vérification si la colonne 'Conso totale (MWh)' existe
        if 'Conso totale (MWh)' in df.columns:
            # Conversion des valeurs en float
            df['Conso totale (MWh)'] = df['Conso totale (MWh)'].str.replace(',', '.').astype(float)
            
            # Calcul de la consommation totale par mois
            conso_mensuelle = df.groupby('mois')['Conso totale (MWh)'].sum()
            
            # Données pour le graphique
            mois_labels = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            y = [conso_mensuelle.get(i, 0) for i in range(1, 13)]
            
            # Création du graphique
            plt.plot(mois_labels, y, marker='o', linestyle='-', color='g', label="Consommation Totale")

            # Personnalisation
            plt.xlabel("Mois")
            plt.ylabel("Consommation Totale (MWh)")
            plt.title("Graphique Annuel de Consommation Totale")
            plt.grid()
            plt.show()
        else:
            print("La colonne 'Conso totale (MWh)' est absente du fichier.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")