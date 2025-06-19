"""
Configuration centralisée du projet.

Ce fichier contient toutes les constantes et paramètres de configuration
nécessaires au fonctionnement des bots Discord et Telegram.

IMPORTANT : Avant d'utiliser le projet, vous devez :
1. Remplacer tous les tokens par vos vrais tokens de bot
2. Configurer les IDs de serveur Discord
3. Définir les listes d'utilisateurs autorisés
4. Vérifier que les chemins de fichiers correspondent à votre structure

Sécurité : Ne jamais commit ce fichier avec de vrais tokens !
"""

# ========================================
# TOKENS D'AUTHENTIFICATION
# ========================================
# Obtenez vos tokens depuis :
# - Telegram : @BotFather sur Telegram
# - Discord : https://discord.com/developers/applications

# Tokens d'authentification des bots
TELEGRAM_BOT_TOKEN = 'REPLACE_WITH_YOUR_TELEGRAM_TOKEN'
TELEGRAM_BOT_TOKEN_SECONDARY = 'REPLACE_WITH_YOUR_TELEGRAM_TOKEN'

DISCORD_BOT_TOKEN = 'REPLACE_WITH_YOUR_DISCORD_TOKEN'
DISCORD_BOT_TOKEN_SECONDARY = 'REPLACE_WITH_YOUR_DISCORD_TOKEN'

# ========================================
# CONFIGURATION SERVEURS
# ========================================

# Identifiants des serveurs
# Pour Discord : Clic droit sur votre serveur > Copier l'ID (Mode développeur requis)
DISCORD_SERVER_ID = 'REPLACE_WITH_YOUR_SERVER_ID'

# ========================================
# CONTRÔLE D'ACCÈS
# ========================================
# Seuls ces utilisateurs peuvent utiliser les bots
# Ajoutez les IDs des utilisateurs autorisés dans ces listes

# Listes des utilisateurs autorisés
AUTHORIZED_TELEGRAM_USERS = []  # IDs Telegram des utilisateurs autorisés
AUTHORIZED_DISCORD_USERS = []   # IDs Discord des administrateurs autorisés

# ========================================
# CHEMINS DE FICHIERS
# ========================================
# Structure des répertoires pour le stockage des données

# Chemins des fichiers de ressources
JSON_FILES_PATH = "ressources/json_files/"                  # Fichiers de configuration globaux
JSON_COMMANDS_PATH = "ressources/json_files/json_command/"  # Fichiers de commandes individuelles
PICTURES_COMMANDS_PATH = "ressources/pictures_command/"     # Photos des commandes Telegram