"""
Gestion des fichiers JSON de commandes individuelles.

Ce module gère les données spécifiques à chaque commande utilisateur :
- Informations client (nom, ID, adresse)
- Détails commande (prix, photo, état)
- Données de traitement (cuisinier assigné, facture, messagerie)

Particularité : Contrairement aux autres modules JSON, celui-ci ne hérite pas
de JsonInherited car chaque commande a son propre fichier JSON unique.

Structure d'une commande :
{
    "user_id": 123456789,
    "username": "john_doe",
    "address": "123 rue Example",
    "price": 15.50,
    "photo_path": "john_doe.jpg",
    "cooker_id": 987654321,
    "facture_message": "Lien de paiement...",
    "instant_messaging": true,
    "ticket_etat": true,
    "command_etat": 0  # 0=en cours, 1=annulée, 2=terminée
}

Accès aux fichiers :
- Par utilisateur : get_command_json(username, user_id, None)
- Par channel Discord : get_command_json(None, None, channel_name)
"""
import json
from typing import Union, List, Optional

from utils.file_management import FileManagement

class CommandJson():

    # Default Command functions
    def get_command_json(username, user_id, channel) -> Optional[dict]:
        """
        Charge les données d'une commande depuis son fichier JSON.

        Args:
            username (str): Nom d'utilisateur Telegram (si accès par utilisateur)
            user_id (int): ID utilisateur Telegram (si accès par utilisateur)
            channel (str): Nom du channel Discord (si accès par channel)

        Returns:
            Optional[dict]: Données de la commande ou None si fichier inexistant

        Deux modes d'accès :
        - Mode utilisateur : username + user_id (depuis Telegram)
        - Mode channel : channel name (depuis Discord)
        """
        data = None

        if channel is None :
            file_path = FileManagement.get_command_json_path(username, user_id)
        else :
            file_path = FileManagement.get_command_json_path_by_channel(channel)

        try :
            with open(file_path, 'r') as file:
                data = json.load(file)
        except :
            print("Le fichier n'existe pas : get_command_json()")

        return data

    def save_command_json(username, user_id, channel, data) -> bool:
        """
        Sauvegarde les données d'une commande dans son fichier JSON.

        Args:
            username (str): Nom d'utilisateur Telegram
            user_id (int): ID utilisateur Telegram
            channel (str): Nom du channel Discord
            data (dict): Données à sauvegarder

        Returns:
            bool: True si sauvegarde réussie

        Important : Utilise l'encodage UTF-8 pour supporter les caractères spéciaux
        dans les noms d'utilisateurs et adresses.
        """
        success = False

        if channel is None :
            file_path = FileManagement.get_command_json_path(username, user_id)
        else :
            file_path = FileManagement.get_command_json_path_by_channel(channel)

        try :
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            success = True
        except :
            print("Le fichier n'existe pas : save_command_json()")

        return success

    def search_command_json_variable(username, user_id, channel, variable) -> Optional[Union[int, str, List]]:
        """
        Recherche une variable spécifique dans une commande.

        Args:
            username (str): Nom d'utilisateur Telegram
            user_id (int): ID utilisateur Telegram
            channel (str): Nom du channel Discord
            variable (str): Nom de la variable à rechercher

        Returns:
            Union[int, str, List]: Valeur de la variable ou None si inexistante

        Exemple : search_command_json_variable("john", 123, None, "command_etat")
        """
        variable_retrieved = None

        data = CommandJson.get_command_json(username, user_id, channel)

        if data is None :
            return

        try :
            variable_retrieved = data.get(variable)
        except :
            print("La variable n'existe pas : search_command_json_variable()")

        return variable_retrieved

    def set_command_json_variable(username, user_id, channel, variable, new_data) -> bool:
        """
        Modifie une variable dans le fichier de commande.

        Args:
            username (str): Nom d'utilisateur Telegram
            user_id (int): ID utilisateur Telegram
            channel (str): Nom du channel Discord
            variable (str): Nom de la variable à modifier
            new_data: Nouvelle valeur à assigner

        Returns:
            bool: True si modification réussie

        Utilisé pour mettre à jour l'état des commandes (command_etat),
        assigner un cuisinier (cooker_id), activer la messagerie, etc.
        """
        success = False

        data = CommandJson.get_command_json(username, user_id, channel)
        if data is not None :

            data[variable] = new_data

            if CommandJson.save_command_json(username, user_id, channel, data) :
                print("Valeur sauvegarder : set_command_json_variable()")
                success = True

        return success

    # Custom functions
    def get_command_json_by_filename(filename) -> Optional[dict]:
        """
        Charge une commande directement par nom de fichier.

        Args:
            filename (str): Chemin complet vers le fichier JSON

        Returns:
            Optional[dict]: Données de la commande

        Utilisé pour parcourir tous les fichiers de commandes
        lors du nettoyage ou des statistiques globales.
        """
        data = None
        try :
            with open(filename, 'r') as file:
                data = json.load(file)
        except :
            print("Le fichier n'existe pas : get_command_json_by_filename()")

        return data

    def set_command_json_facture_message(username, user_id, new_message) -> bool:
        """
        Configure le message de facture pour une commande.

        Args:
            username (str): Nom d'utilisateur Telegram
            user_id (int): ID utilisateur Telegram
            new_message (str): Message de facture personnalisé ou None pour défaut

        Returns:
            bool: True si configuration réussie

        Le message de facture est envoyé à l'utilisateur Telegram quand
        l'administrateur Discord génère la facture de la commande.
        """
        # Modifier la variable new_message permet un de modifier le message de la facture sinon celui par défault est appliqué
        # La sauvegarde de la facture permet la reception dans telegram

        success = False

        if new_message is None :
            new_message = f"Vous pouvez regler le montant de votre commande a ce lien la : https://www.example.com/"

        success = CommandJson.set_command_json_variable(username, user_id, None, "facture_message", new_message)

        return success

# Exemple d'utilisation

# data = CommandJson.get_command_json("Yann p", "62205925", None)
# print(data)
# print(CommandJson.search_command_json_variable("Yann p", "62205925", None, "photo_path"))
# CommandJson.set_command_json_variable("Yann p", "62205925", None, "photo_path", "photo_de_pomme.jpg")
# CommandJson.set_command_json_facture_message("Yann p", "62205925", None)