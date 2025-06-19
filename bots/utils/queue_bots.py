"""
Système de communication inter-bots via des queues partagées.

Cette classe permet aux bots Discord et Telegram de communiquer entre eux
de manière asynchrone sans dépendances directes. Chaque bot a sa propre queue
pour recevoir des messages de l'autre bot.

Architecture :
- Bot Discord envoie des messages vers queue_telegram
- Bot Telegram envoie des messages vers queue_discord
- Les queues sont thread-safe pour éviter les conflits
"""

from queue import Queue

class QueueBot():
    """
    Gestionnaire des queues de communication inter-bots.

    Permet la synchronisation des commandes entre Discord (administrateurs)
    et Telegram (utilisateurs) sans couplage direct entre les modules.
    """

    def __init__(self) -> None:
        # Queue pour les messages destinés au bot Telegram
        self.queue_telegram = Queue()
        # Queue pour les messages destinés au bot Discord
        self.queue_discord = Queue()

    def get_queue_telegram(self) -> Queue:
        # Retourne la queue pour envoyer des messages vers Telegram.
        return self.queue_telegram

    def get_queue_discord(self) -> Queue:
        # Retourne la queue pour envoyer des messages vers Discord.
        return self.queue_discord
