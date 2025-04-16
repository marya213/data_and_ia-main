from energie import Moyen_Consommation, Total_Consommation, Consommation_Par_Habitant, Graphique_Consommation_Mensuelle
from meteo import meteo_display_temperature_on_data , Graphique_Température_Annuelle
import pandas as pd


        
def main():
        # Consommation Moyenne
        moyenne = Moyen_Consommation("/home/garcon/Documents/gitlab/data_and_ia/src/data/data_énergie_trié_modifié.csv", 'Conso totale (MWh)')
        print(f"\n - La consommation moyenne est de {moyenne} MWh sur la Commune de Rennes")

        # Consommation Totale
        total = Total_Consommation("/home/garcon/Documents/gitlab/data_and_ia/src/data/data_énergie_trié_modifié.csv", 'Conso totale (MWh)')
        print(f"\n - La consommation totale est de {total} MWh sur la Commune de Rennes")

        # Consommation par habitant
        moyenne_par_habitant, total_par_habitant = Consommation_Par_Habitant("/home/garcon/Documents/gitlab/data_and_ia/src/data/data_énergie_trié_modifié.csv")
        print(f"\n - La consommation moyenne par habitant est de {moyenne_par_habitant} MWh")
        print(f"\n - La consommation totale par habitant est de {total_par_habitant} MWh")
        
        try:
            meteo_display_temperature_on_data("/home/garcon/Documents/gitlab/data_and_ia/src/data/donne_meteorologique.csv", "2013-04-06")
        except FileNotFoundError:
            print("Le fichier 'donne_meteorologique.csv' est introuvable. Veuillez vérifier le chemin ou l'emplacement du fichier.")
            
            
        Graphique_Température_Annuelle("/home/garcon/Documents/gitlab/data_and_ia/src/data/donne_meteorologique.csv")
        
        Graphique_Consommation_Mensuelle("/home/garcon/Documents/gitlab/data_and_ia/src/data/eCO2mix_RTE_tempo_2023-2024.csv")
        
    # Exemple d'utilisation 
main()
