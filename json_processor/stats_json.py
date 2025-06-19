"""
Gestion des statistiques globales du service.

Ce module suit les métriques importantes du business :
- Chiffre d'affaires total (argent cumulé)
- Nombre total de commandes traitées
- Autres indicateurs de performance

Structure JSON :
{
    "argent_cumule": 125.50,
    "nombre_commande": 25
}

Utilisation :
- Mise à jour automatique à chaque commande terminée
- Consultation via la commande Discord !stats
- Suivi de la croissance du service
"""

from json_processor.json_inherited import JsonInherited
from utils.constants import JSON_FILES_PATH

class StatsJson(JsonInherited):
    """
    Gestionnaire des statistiques globales du service.

    Centralise tous les indicateurs de performance pour
    le suivi et l'analyse du business.
    """
    filename = JSON_FILES_PATH + "stats.json"

    ##
    # Variables fichier json : argent_cumule:float, nombre_commande:float
    ##

    # Custom functions
    def update_total_money(price) -> bool:
        """
        Met à jour le chiffre d'affaires total.

        Args:
            price (float): Montant de la commande à ajouter

        Returns:
            bool: True si mise à jour réussie

        Appelée automatiquement quand une commande est facturée
        pour maintenir le total des revenus à jour.
        """
        success  = False

        stats_data = StatsJson.get_json_file()
        argent_cumule = stats_data.get("argent_cumule")

        if argent_cumule is not None:
            argent_cumule = float(argent_cumule) + float(price)
            stats_data["argent_cumule"] = argent_cumule
            StatsJson.save_json_file(stats_data)
        else:
            print("La variable est introuvable")

        return success

    def add_a_command() -> bool:
        """
        Incrémente le compteur de commandes traitées.

        Returns:
            bool: True si incrémentation réussie

        Appelée chaque fois qu'une nouvelle commande est créée
        pour suivre le volume d'activité.
        """
        success  = True

        data = StatsJson.get_json_file()
        if data is not None:
            try :
                data["nombre_commande"] =  data.get("nombre_commande") + 1
                StatsJson.save_json_file(data)
            except:
                success = False

        return success

# Exemple d'utilisation

# data = StatsJson.get_json_file()
# print(data)
# StatsJson.update_total_money(10)
# data = StatsJson.get_json_file()
# print(data)