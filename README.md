# Bots Discord & Telegram

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.0.0+-green.svg)
![Python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-13.0+-yellow.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

*Système de bots interconnectés pour la gestion de commandes entre Discord et Telegram*

</div>

---

## 📋 Présentation

Ce projet implémente un système de bots interconnectés permettant la gestion de commandes entre Discord et Telegram. Les utilisateurs passent commande via Telegram, tandis que les administrateurs gèrent les commandes via Discord.

### ✨ Fonctionnalités principales

- **Système de commandes** : Prise de commande via Telegram avec photos et adresses
- **Gestion administrative** : Interface Discord pour traiter les commandes
- **Communication temps réel** : Messagerie instantanée entre les plateformes
- **Système de fidélité** : Points de fidélité et classements
- **Statistiques** : Suivi du chiffre d'affaires et des commandes
- **Liste noire** : Gestion des utilisateurs bloqués

## 🛠️ Technologies

- **Python 3.8+** - Langage principal
- **discord.py** - Bot Discord
- **python-telegram-bot** - Bot Telegram 
- **JSON** - Stockage des données
- **asyncio** - Gestion asynchrone

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- Compte Discord Developer avec bot créé
- Compte Telegram Bot via @BotFather

### Installation rapide

```bash
# Cloner le projet
git clone https://github.com/Y-Picot/messagerie-instantanee-bots-discord-telegram.git
cd bots-discord-telegram

# Installation
pip install .
```

### Configuration

Modifiez le fichier `utils/constants.py` :

```python
# Tokens des bots
TELEGRAM_BOT_TOKEN = 'VOTRE_TOKEN_TELEGRAM'
DISCORD_BOT_TOKEN = 'VOTRE_TOKEN_DISCORD'

# Configuration serveur
DISCORD_SERVER_ID = 'ID_DE_VOTRE_SERVEUR_DISCORD'

# Utilisateurs autorisés
AUTHORIZED_TELEGRAM_USERS = [123456789]
AUTHORIZED_DISCORD_USERS = [123456789]
```

## 🚀 Utilisation

### Démarrage

```bash
python main.py
```

### Commandes Discord

| Commande | Description |
|----------|-------------|
| `!test` | Teste la connexion |
| `!editer_annonce [message]` | Définit le message d'annonce |
| `!facture` | Génère une facture |
| `!fermer_commande` | Ferme une commande |
| `!stats` | Affiche les statistiques |
| `!classement` | Top 10 fidélité |

### Commandes Telegram

| Commande | Description |
|----------|-------------|
| `/start` | Démarre la conversation |
| `/annuler_commande` | Annule une commande |
| `/facture` | Consulte la facture |

## 🏗️ Architecture

```
├── bots/                  # Modules des bots
├── interfaces/            # Boutons et embeds
├── json_processor/        # Gestion des données JSON
├── ressources/            # Fichiers de données
├── utils/                 # Utilitaires généraux
└── main.py                # Point d'entrée
```

Le système utilise une **queue partagée** pour synchroniser les communications entre Discord et Telegram en temps réel.

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre [Guide de Contribution](CONTRIBUTING.md) pour plus de détails.

Étapes rapides :

1. Forker le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Ouvrir une Pull Request

📖 **Ressources pour les contributeurs :**
- [Guide d'Installation](docs/INSTALLATION.md) - Configuration de l'environnement
- [Guide de Développement](docs/guide-developpement.md) - Architecture et bonnes pratiques

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

**Développé par [Y-Picot](https://github.com/Y-Picot) & [axboulangerr](https://github.com/axboulangerr)**

⭐ N'hésitez pas à donner une étoile si ce projet vous a été utile !

</div>

