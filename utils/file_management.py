"""
Gestion centralisée des fichiers et des noms de fichiers du projet.

Ce module fournit des utilitaires pour :
- Formater les noms d'utilisateurs pour les noms de fichiers/channels
- Gérer les chemins des fichiers JSON et images
- Extraire des informations depuis les noms de channels Discord
- Nettoyer les fichiers de commandes terminées

Convention de nommage :
- Channels Discord : "command_username_userid"
- Fichiers JSON : "command_username_userid.json"
- Images : "username.jpg"
"""
from typing import Optional, Tuple
import os

from utils.constants import PICTURES_COMMANDS_PATH, JSON_COMMANDS_PATH

class FileManagement():
    """
    Classe utilitaire pour la gestion des fichiers et noms de fichiers.

    Centralise toute la logique de nommage et de manipulation des fichiers
    pour maintenir la cohérence à travers le projet.
    """

    # Format
    def format_username(username) -> Optional[str]:
        """
        Formate un nom d'utilisateur pour l'utiliser dans les noms de fichiers.

        Transforme "John Doe" en "john-doe" pour éviter les problèmes
        avec les espaces dans les noms de fichiers et channels Discord.
        """
        return (username.replace(" ", "-")).lower()

    def format_username_userid(username, user_id) -> str:
        """
        Combine le nom d'utilisateur formaté avec son ID unique.

        Exemple : "John Doe" + 123456 -> "john-doe_123456"
        Ceci garantit l'unicité même si deux utilisateurs ont le même nom.
        """
        formated_username = FileManagement.format_username(username)
        return formated_username+"_"+str(user_id)

    def format_well_formed(filename) -> bool:
        """
        Vérifie si un nom de fichier respecte les conventions du projet.

        Format attendu : "command_username_userid.json"
        Cette vérification évite de traiter des fichiers non conformes.
        """
        # Normalement inutile puisque le dossier ne contient exclusivement des fichiers crées par le programme.
        # Ici utiliser parce qu'un exemple du jeu de donnée est contenu dans le dossier.

        is_well_formed = True

        split_filename = filename.split("_")
        if len(split_filename) != 3 or split_filename[0] != "command":
            is_well_formed = False

        return is_well_formed

    def get_command_channel_name(username, user_id) -> str:
        """
        Génère le nom du channel Discord pour une commande.

        Chaque commande utilisateur crée un channel privé sur Discord
        pour que les administrateurs puissent la traiter.
        """
        username_userid = FileManagement.format_username_userid(username, user_id)
        return f"command_{username_userid}"

    def get_command_json_file_name(username, user_id) -> str:
        """
        Génère le nom du fichier JSON pour sauvegarder une commande.

        Chaque commande est sauvegardée dans un fichier JSON séparé
        pour éviter les conflits et faciliter la gestion.
        """
        username_userid = FileManagement.format_username_userid(username, user_id)
        return f"command_{username_userid}.json"

    def get_command_jpg_file_name(username) -> str:
        """
        Génère le nom du fichier image pour une commande.

        Les utilisateurs Telegram envoient une photo de leur commande
        qui est sauvegardée avec ce nom formaté.
        """
        username_userid = FileManagement.format_username(username)
        return f"{username_userid}.jpg"

    # Extraction d'information
    def get_username_userid_from_channel_name(channel) -> Tuple[Optional[int], Optional[str]]:
        """
        Extrait le nom d'utilisateur et l'ID depuis un nom de channel Discord.

        Permet de retrouver les informations utilisateur depuis le nom
        du channel Discord pour traiter les commandes.
        """
        username = None
        user_id = None

        if channel is not None and channel.startswith("command_") :
            username, user_id = (channel.split("_"))[1:3] # Récupère élèment 1 et 2
        else :
            print("Le channel n'existe pas : extract_username_userid_from_channel_name()")
        return username, user_id

    def get_userid_from_channel_name(message) -> Optional[str]:
        """
        Récupère uniquement l'ID utilisateur depuis un nom de channel.

        Utile pour identifier rapidement l'utilisateur concerné
        par une action dans un channel Discord.
        """
        # Le channel étant écrit sous ce format command_username_userid. On récupère les trois parties et on garde l'userid
        split_destinataire = message.split("_")
        return split_destinataire[len(split_destinataire) - 1]

    # PATH
    def get_command_json_path(username, user_id) -> str:
        """
        Retourne le chemin complet vers le fichier JSON d'une commande.

        Combine le répertoire de base avec le nom de fichier formaté
        pour obtenir le chemin absolu du fichier de commande.
        """
        return JSON_COMMANDS_PATH + FileManagement.get_command_json_file_name(username, user_id)

    def get_command_json_path_by_channel(channel) -> str:
        """
        Retourne le chemin JSON depuis un nom de channel Discord.

        Permet d'accéder au fichier de commande directement depuis
        le contexte d'un channel Discord sans connaître l'utilisateur.
        """
        return JSON_COMMANDS_PATH + channel + ".json"

    def get_command_jpg_path(username) -> str:
        """
        Retourne le chemin complet vers l'image d'une commande.

        Les photos de commandes Telegram sont stockées dans un répertoire
        dédié avec un nom basé sur l'utilisateur.
        """
        formated_username = FileManagement.get_command_jpg_file_name(username)
        return PICTURES_COMMANDS_PATH + formated_username

    # Remove
    def remove_command_files(username, user_id) -> bool:
        """
        Supprime tous les fichiers associés à une commande terminée.

        Nettoie le fichier JSON et l'image pour libérer l'espace disque
        une fois la commande traitée et archivée.
        """
        success = False
        try :
            format_command_json_path = FileManagement.get_command_json_path(username, user_id)
            format_jpg_path = FileManagement.get_command_jpg_path(username)
            os.remove(format_command_json_path)
            os.remove(format_jpg_path)
            success = True
        except :
            print("Un des fichiers n'existe pas : remove_command_files()")
        return success

# print(FileManagement.get_username_userid_from_channel_name("command_yann-p_925525"))
