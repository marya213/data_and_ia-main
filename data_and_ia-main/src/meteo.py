import pandas as pd
import matplotlib.pyplot as plt

def meteo_display_temperature_on_data(input_file, date):
    # Affichage de la température en fonction de la date
    df = pd.read_csv(input_file, encoding='ISO-8859-1', header=0)
    
    try:
        # Conversion de la colonne 'Date' en format datetime pour faciliter la recherche
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)
        df = df.set_index('Date')
        
        # Vérification si la date est présente dans l'index
        if pd.Timestamp(date).tz_localize('UTC') in df.index:
            data = df.loc[pd.Timestamp(date).tz_localize('UTC')]
            if isinstance(data, pd.Series):  # Vérifie si une seule ligne correspond à la date
                temperature = data.get('Temperature', None)
                if temperature is not None:
                    print(f"Température pour la date {date} : {temperature}°C")
                else:
                    print(f"Aucune colonne 'Température (°C)' trouvée dans les données pour la date {date}.")
            else:  # Plusieurs lignes correspondent à la date
                if 'Température (°C)' in data.columns:
                    print(f"Températures pour la date {date} :")
                    print(data['Température (°C)'])
                else:
                    print(f"Aucune colonne 'Température (°C)' trouvée dans les données pour la date {date}.")
        else:
            print(f"Aucune donnée disponible pour la date {date}.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        
def Graphique_Température_Annuelle(input_file):
    # Lecture du fichier CSV
    df = pd.read_csv(input_file, encoding='ISO-8859-1', header=0)
    
    try:
        # Conversion de la colonne 'Date' en format datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)
        df['mois'] = df['Date'].dt.month  # Extraction du mois
        
        # Vérification si la colonne 'Température (°C)' existe
        if 'Temperature' in df.columns:
            # Calcul de la température moyenne par mois
            moyen_temp_mensuelle = df.groupby('mois')['Temperature'].mean()
            
            # Données pour le graphique
            mois_labels = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                           "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            y = [moyen_temp_mensuelle.get(i, None) for i in range(1, 13)]
            
            # Création du graphique
            plt.plot(mois_labels, y, marker='o', linestyle='-', color='b', label="Température Moyenne")

            # Personnalisation
            plt.xlabel("Mois")
            plt.ylabel("Température Moyenne (°C)")
            plt.title("Graphique Annuel de Température Moyenne")
            # plt.legend()
            plt.grid()
            plt.show()
        else:
            print("La colonne 'Température (°C)' est absente du fichier.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")