"""
Interface des boutons Telegram pour les annonces.

Ce module génère les boutons interactifs des annonces Telegram :
- Bouton "Order" : Pour passer une commande
- Bouton "Proof" : Pour demander une preuve de qualité

Fonctionnalités :
- Génération d'ID unique pour chaque annonce
- Suivi des interactions utilisateur
- Intégration avec le système de callbacks Telegram
"""

import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import json_processor.announcement_json as AJ


class ButtonTelegram():
    """
    Générateur de boutons pour les annonces Telegram.

    Chaque annonce a des boutons uniques identifiés par un timestamp
    pour éviter les conflits entre différentes sessions d'annonces.
    """

    def __init__(self)  -> None:
        """
        Initialise les boutons avec un ID unique basé sur le timestamp.

        L'ID unique permet de :
        - Différencier les annonces multiples
        - Éviter les interactions croisées
        - Suivre les statistiques par annonce
        """
        self.unique_id = str(int(time.time()))
        AJ.AnnouncementJson.set_json_variable("last_announce_id", self.unique_id)

        # Création des boutons avec callbacks uniques
        keyboard = [
            [InlineKeyboardButton("💵 Order", callback_data=f"order-{self.unique_id}"),
            InlineKeyboardButton("🔥 Proof", callback_data=f"order-{self.unique_id}")]
        ]
        self.reply_markup = InlineKeyboardMarkup(keyboard)

    def get_button_order_proof(self) -> InlineKeyboardMarkup:
        """
        Retourne les boutons formatés pour l'envoi Telegram.

        Returns:
            InlineKeyboardMarkup: Boutons prêts à être envoyés avec un message

        Utilisé dans les fonctions d'envoi d'annonces pour attacher
        les boutons interactifs aux messages.
        """
        return self.reply_markup