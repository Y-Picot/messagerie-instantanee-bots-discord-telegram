"""
Point d'entrée principal pour les bots Discord et Telegram.

Ce module lance les deux bots en utilisant un système de queue partagée
pour permettre la communication inter-bots sans dépendances directes.

WORKFLOW GLOBAL :
1. Les utilisateurs Telegram passent des commandes (photo + adresse + prix)
2. Les commandes sont transmises au Discord des administrateurs
3. Les administrateurs Discord prennent en charge, facturent ou annulent
4. Les actions sont synchronisées vers Telegram en temps réel
5. Les points de fidélité et statistiques sont mis à jour automatiquement

ARCHITECTURE :
- Thread principal : Bot Telegram (premier lancé)
- Thread secondaire : Bot Discord (lancé après Telegram)
- Communication : Queue partagée thread-safe
- Persistance : Fichiers JSON avec encodage UTF-8

PRÉREQUIS :
- Tokens bot configurés dans utils/constants.py
- Répertoires ressources/ créés avec les fichiers JSON
- Permissions bot Discord (gestion channels, messages, fichiers)
- Bot Telegram configuré avec @BotFather
"""

import logging
from bots.discord_bot import run_discord_bot
from bots.telegram_bot import run_telegram_bot
from bots.utils.queue_bots import QueueBot

# Configuration des logs pour le debug et monitoring
logging.basicConfig(
    filename='bot_logs.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    # Initialisation de la queue partagée entre les bots
    # Cette queue permet la communication asynchrone entre Discord et Telegram
    queue_bots = QueueBot()

    # Démarrage des bots Telegram et Discord
    # ORDRE IMPORTANT : Telegram en premier, puis Discord
    # Discord est déclaré en deuxième pour éviter les conflits de threads
    run_telegram_bot(queue_bots)
    run_discord_bot(queue_bots)
