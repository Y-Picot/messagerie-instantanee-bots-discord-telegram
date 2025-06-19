# 🚀 Guide d'Installation Détaillé

Ce guide vous accompagne pas à pas pour installer et configurer les bots Discord et Telegram.

## 📋 Prérequis

### 1. Environnement Python
```bash
# Vérifier la version Python (3.8+ requis)
python --version

# Si Python n'est pas installé, téléchargez depuis python.org
```

### 2. Créer un Bot Discord
1. Allez sur https://discord.com/developers/applications
2. Créez une nouvelle application
3. Dans l'onglet "Bot", créez un bot
4. Copiez le token (gardez-le secret !)
5. Invitez le bot sur votre serveur avec les permissions :
   - Gérer les canaux
   - Envoyer des messages  
   - Joindre des fichiers
   - Utiliser les commandes slash

### 3. Créer un Bot Telegram
1. Contactez @BotFather sur Telegram
2. Utilisez `/newbot` pour créer un bot
3. Suivez les instructions pour nommer votre bot
4. Copiez le token fourni par BotFather

## 🔧 Installation

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd messagerie-instantanee-bots-discord-bots-telegram
```

### 2. Installer les dépendances
```bash
# Option 1 : Avec pip
pip install discord.py python-telegram-bot

# Option 2 : Avec requirements.txt (si vous en créez un)
pip install -r requirements.txt
```

### 3. Configuration des tokens

Modifiez `utils/constants.py` :

```python
# Remplacez par vos vrais tokens
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN_HERE'
DISCORD_BOT_TOKEN = 'YOUR_DISCORD_BOT_TOKEN_HERE'

# ID de votre serveur Discord (clic droit > Copier l'ID)
DISCORD_SERVER_ID = '123456789012345678'

# IDs des utilisateurs autorisés
AUTHORIZED_TELEGRAM_USERS = [123456789]  # Votre ID Telegram
AUTHORIZED_DISCORD_USERS = [123456789]   # Votre ID Discord
```

### 4. Créer la structure des fichiers

Le projet a besoin de fichiers JSON initiaux dans `ressources/json_files/` :

```bash
# Les fichiers suivants doivent exister :
ressources/json_files/announce.json
ressources/json_files/blacklist.json  
ressources/json_files/loyalty.json
ressources/json_files/stats.json
```

Contenu initial des fichiers :

**announce.json** :
```json
{
    "announce_message": "Nouvelle annonce de livraison disponible !",
    "last_announce_id": "1000000000"
}
```

**blacklist.json** :
```json
{
    "List": []
}
```

**loyalty.json** :
```json
[]
```

**stats.json** :
```json
{
    "argent_cumule": 0.0,
    "nombre_commande": 0
}
```

## 🏃 Premier lancement

### 1. Tester la configuration
```bash
python main.py
```

Si tout fonctionne, vous devriez voir les bots se connecter sans erreurs.

### 2. Tester les commandes

**Sur Discord** :
- `!test` - Vérifier que le bot répond
- `!help` - Voir toutes les commandes disponibles

**Sur Telegram** :
- `/start` - Démarrer la conversation avec le bot

## 🐛 Résolution des problèmes courants

### Erreur de token
```
discord.errors.LoginFailure: Improper token has been passed
```
➜ Vérifiez que votre token Discord est correct dans `constants.py`

### Erreur de permissions Discord
```
Forbidden (status code: 403)  
```
➜ Assurez-vous que le bot a les permissions nécessaires sur votre serveur

### Fichiers JSON manquants
```
FileNotFoundError: [Errno 2] No such file or directory
```
➜ Créez les fichiers JSON avec la structure décrite ci-dessus

### Import discord non trouvé
```
ModuleNotFoundError: No module named 'discord'
```
➜ Installez discord.py : `pip install discord.py`

## 🔒 Sécurité

⚠️ **IMPORTANT** :
- Ne jamais commiter vos tokens dans Git
- Utilisez des variables d'environnement en production
- Gardez vos tokens secrets et ne les partagez jamais

## 📚 Ressources utiles

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Python Telegram Bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Guide des permissions Discord](https://discord.com/developers/docs/topics/permissions)

---

Une fois l'installation terminée, consultez le [Guide de Développement](docs/guide-developpement.md) pour comprendre l'architecture du projet.
