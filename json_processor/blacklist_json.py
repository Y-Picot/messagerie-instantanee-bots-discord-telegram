"""
Gestion de la liste noire des utilisateurs.

Ce module permet de bannir des utilisateurs qui abusent du système
ou violent les règles d'utilisation. Les utilisateurs en liste noire
ne peuvent plus passer de nouvelles commandes.

Structure JSON :
{
    "List": [123456789, 987654321, ...]
}

Fonctionnalités :
- Ajouter un utilisateur à la liste noire
- Retirer un utilisateur de la liste noire
- Vérifier si un utilisateur est banni
"""

from json_processor.json_inherited import JsonInherited
from utils.constants import JSON_FILES_PATH

class BlacklistJson(JsonInherited):
    """
    Gestionnaire de la liste noire des utilisateurs.

    Utilise les IDs Telegram des utilisateurs pour les identifier
    de manière unique et éviter les contournements par changement de nom.
    """
    filename = JSON_FILES_PATH + "blacklist.json"

    # "List": [int]

    # Custom functions
    def add_to_blacklist(user_id) -> bool:
        """
        Ajoute un utilisateur à la liste noire.

        Args:
            user_id (int): ID Telegram de l'utilisateur à bannir

        Returns:
            bool: True si ajouté avec succès, False si déjà présent

        L'utilisateur ne pourra plus passer de nouvelles commandes.
        """
        success = False
        data = BlacklistJson.get_json_file()
        if BlacklistJson.is_userid_in_blacklist :
            data["List"].append(user_id)
            BlacklistJson.save_json_file(data)
            success = True
        else :
            print("Utilisateur déjà dans la blacklist : add_to_blacklist()")
        return success

    def delete_from_blacklist(user_id) -> bool:
        """
        Retire un utilisateur de la liste noire.

        Args:
            user_id (int): ID Telegram de l'utilisateur à débannir

        Returns:
            bool: True si retiré avec succès, False si erreur

        L'utilisateur pourra à nouveau passer des commandes.
        """
        success = False
        data = BlacklistJson.get_json_file()
        try :
            data["List"].remove(user_id)
            BlacklistJson.save_json_file(data)
            success = True
        except :
            print("List.remove a planté : delete_from_blacklist()")

        return success

    def is_userid_in_blacklist(user_id) -> bool:
        """
        Vérifie si un utilisateur est dans la liste noire.

        Args:
            user_id (int): ID Telegram à vérifier

        Returns:
            bool: True si banni, False si autorisé

        Cette fonction est appelée avant de traiter chaque nouvelle commande.
        """
        success = False
        data = BlacklistJson.get_json_file()
        if user_id in data.get("List"):
            success = True

        return success


# Exemple d'utilisation
# data = BlacklistJson.get_json_file()
# print(data["List"])
# BlacklistJson.add_to_blacklist(333)
# BlacklistJson.delete_from_blacklist(333)
