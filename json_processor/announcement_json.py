"""
Gestion des annonces globales du service.

Ce module stocke le message d'annonce diffusé à tous les utilisateurs Telegram
ainsi que l'ID de la dernière annonce pour éviter les doublons.

Structure JSON :
{
    "announce_message": "Nouvelle annonce de livraison disponible !",
    "last_announce_id": "1000000000"
}

Fonctionnalités :
- Stockage du message d'annonce global
- Suivi des IDs d'annonce pour éviter les doublons
- Modification du message via les commandes Discord
"""

from json_processor.json_inherited import JsonInherited
from utils.constants import JSON_FILES_PATH

class AnnouncementJson(JsonInherited):
    """
    Gestionnaire des annonces globales diffusées aux utilisateurs.

    Centralise le contenu des annonces et leur identifiant unique
    pour coordonner la diffusion entre Discord et Telegram.
    """
    filename = JSON_FILES_PATH + "announce.json"

    # announce_message:str

# Exemple d'utilisation
# from announcement_json import AnnouncementJson

# data = AnnouncementJson.get_json_file()
# print(data)