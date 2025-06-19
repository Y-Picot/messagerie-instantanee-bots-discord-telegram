"""
Interface des boutons Discord pour la gestion des commandes.

Ce module centralise tous les boutons interactifs des embeds Discord :
- Prendre en charge une commande (vert)
- Supprimer une commande (rouge)
- Ajouter à la liste noire (bleu)

Architecture :
- Chaque bouton hérite de discord.ui.Button
- Les actions sont gérées dans les callbacks
- L'état des commandes est synchronisé via les fichiers JSON
"""

import discord

from interfaces.button_delete_command import ButtonDeleteCommand
from interfaces.button_create_command import ButtonCreateCommand
from interfaces.button_add_to_blacklist import ButtonAddToBlacklist

class ButtonsStyle(discord.ui.View):
    """
    Vue Discord contenant tous les boutons d'action pour une commande.

    Cette classe groupe les trois boutons principaux que les administrateurs
    Discord peuvent utiliser pour traiter les commandes des utilisateurs Telegram.
    """

    def __init__(self, username, user_id)  -> None:
        """
        Initialise la vue avec les boutons pour une commande spécifique.

        Args:
            username (str): Nom d'utilisateur Telegram du client
            user_id (int): ID Telegram unique du client

        Les boutons sont liés à l'utilisateur pour les actions ciblées.
        """
        super().__init__()
        # Créer des instances de boutons personnalisés
        delete_button = ButtonDeleteCommand(username, user_id)
        create_button = ButtonCreateCommand()
        blacklist_button = ButtonAddToBlacklist(username, user_id)

        # Ajouter les boutons à la vue
        self.add_item(create_button)    # Bouton vert : "Prendre la commande"
        self.add_item(delete_button)    # Bouton rouge : "Supprimer la commande"
        self.add_item(blacklist_button) # Bouton bleu : "Mettre en liste noire"
