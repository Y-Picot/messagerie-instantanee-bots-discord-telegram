"""
Gestion du système de points de fidélité.

Ce module récompense les utilisateurs réguliers en leur attribuant des points
à chaque commande réussie. Les points peuvent être utilisés pour des réductions
ou des avantages spéciaux.

Structure JSON :
[
    {
        "user_id": 123456789,
        "username": "john_doe",
        "points": 15
    },
    ...
]

Fonctionnalités :
- Attribution automatique de points à chaque commande
- Consultation du solde de points d'un utilisateur
- Classement des utilisateurs par points (leaderboard)
"""

from typing import Optional

from json_processor.json_inherited import JsonInherited
from utils.constants import JSON_FILES_PATH

class LoyaltyJson(JsonInherited):
    """
    Gestionnaire du système de points de fidélité.

    Chaque commande terminée avec succès rapporte 1 point au client.
    Les points sont liés à l'ID Telegram pour éviter les doublons.
    """

    # Attribut non instancié
    filename = JSON_FILES_PATH + "loyalty.json"
    id_name = "user_id"

    ##
    # Liste du fichier JSON composé de :
    #       - user_id:int,
    #       - username:str,
    #       - points:int
    ##

    # Custom functions
    def add_a_point(username, user_id) -> bool:
        """
        Ajoute un point de fidélité à un utilisateur.

        Args:
            username (str): Nom d'utilisateur Telegram
            user_id (int): ID unique Telegram

        Returns:
            bool: True si le point a été ajouté avec succès

        Si l'utilisateur n'existe pas, il est créé avec 1 point.
        Si il existe déjà, ses points sont incrémentés de 1.
        """
        success = True

        user_finded = False
        data = LoyaltyJson.get_json_file()
        if data is None :
            success = False

        # Trouver l'utilisateur dans le fichier loyalty.json
        for user in data :
            if user["username"] == username or user["user_id"] == user_id: # Si trouvé lui ajoute un point
                user["points"] = user.get("points") + 1
                user_finded = True

        # Sinon créer un nouvel utilisateur dans le fichier loyalty.json
        if not user_finded :
            try :
                element_new = {
                    "user_id": user_id,
                    "username": username,
                    "points": 1
                }

                data.append(element_new) # Et l'ajoute au fichier
            except:
                success = False

        if not LoyaltyJson.save_json_file(data):
            success = False

        return success

    def get_points_user(username) -> Optional[int]:
        """
        Récupère le nombre de points d'un utilisateur.

        Args:
            username (str): Nom d'utilisateur Telegram

        Returns:
            Optional[int]: Nombre de points ou None si utilisateur inexistant

        Utilisé pour afficher le solde de points à l'utilisateur
        et pour le classement général.
        """
        user_points = None

        data = LoyaltyJson.get_json_file()
        for user in data :
            if user["username"] == username:
                user_points = user.get("points")

        return user_points

# Exemple d'utilisation

# data = LoyaltyJson.get_json_file()
# print(data)

# element_new = {
#     "user_id": 245123542255,
#     "points": 30
# }

# print(LoyaltyJson.get_json_element_from_list(2553536626))
# LoyaltyJson.add_json_element_to_list(element_new)

# data = LoyaltyJson.get_json_file()
# print(data)

# LoyaltyJson.delete_json_element_to_list(2553536626)

# LoyaltyJson.add_a_point("Poulette-de-Angelo", 25266262)
# print(LoyaltyJson.get_json_element_from_list(245123542255))
# print(LoyaltyJson.get_points_user("Poulette-de-Angelo"))