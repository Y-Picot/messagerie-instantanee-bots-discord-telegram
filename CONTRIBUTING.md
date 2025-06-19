# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! Ce guide vous explique comment participer efficacement.

## 🚀 Premiers pas

### 1. Comprendre le projet
- Lisez le [README.md](../README.md) pour une vue d'ensemble
- Consultez le [Guide d'Installation](docs/INSTALLATION.md) pour configurer votre environnement
- Parcourez le [Guide de Développement](docs/guide-developpement.md) pour comprendre l'architecture

### 2. Configuration de développement
```bash
# Fork du projet sur GitHub
# Clone de votre fork
git clone https://github.com/Y-Picot/messagerie-instantanee-bots-discord-telegram.git
cd messagerie-instantanee-bots-discord-bots-telegram

# Configuration des tokens de test
# Utilisez des bots de développement différents de la production
```
## 🎯 Types de contributions acceptées

### 🐛 Correction de bugs
- Reproduisez le bug de manière fiable
- Décrivez les étapes pour le reproduire
- Proposez une solution avec tests

### ✨ Nouvelles fonctionnalités
- Discutez d'abord dans une issue GitHub
- Respectez l'architecture existante (JSON, threads séparés)
- Ajoutez de la documentation

### 📝 Documentation
- Commentaires pédagogiques en français
- Exemples d'utilisation
- Guides d'installation et configuration

### 🧹 Amélioration du code
- Optimisations des TODO listés dans le guide de développement
- Refactoring respectant les patterns existants
- Tests unitaires

## 📋 Standards de code

### Conventions Python
```python
# Noms de fonctions en snake_case
def format_username(username):
    pass

# Commentaires pédagogiques en français
def add_to_blacklist(user_id):
    """
    Ajoute un utilisateur à la liste noire.
    
    Args:
        user_id (int): ID Telegram de l'utilisateur à bannir
    """

# Encodage UTF-8 obligatoire pour tous les fichiers JSON
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
```

### Gestion des imports circulaires
```python
# Pattern à respecter pour éviter les imports circulaires
import nom_fichier as nom
# Utilisation : nom.class.fonction
```

### Structure des commits
```
type(scope): description courte

Description plus détaillée si nécessaire.

Fixes #123
```

Types acceptés : `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## 🔄 Workflow de contribution

### 1. Préparer votre contribution
```bash
# Créer une branche pour votre feature
git checkout -b feature/ma-nouvelle-fonctionnalite

# Ou pour un bugfix
git checkout -b fix/correction-bug-xyz
```

### 2. Développer
- Respectez l'architecture existante (cf. guide de développement)
- Ajoutez des commentaires pédagogiques en français
- Testez localement avec vos bots de développement

### 3. Tests recommandés
- Test manuel des fonctionnalités modifiées
- Vérification de la synchronisation Discord ↔ Telegram
- Test de l'encodage UTF-8 des fichiers JSON

### 4. Soumettre
```bash
# Commit de vos changements
git add .
git commit -m "feat(telegram): ajout délai anti-spam"

# Push vers votre fork
git push origin feature/ma-nouvelle-fonctionnalite

# Créer une Pull Request sur GitHub
```

## 🎯 Priorités de développement

Consultez les TODO dans le [Guide de Développement](docs/guide-developpement.md) :

### 🔧 **Options prioritaires**
- [ ] Main : relance des threads
- [ ] Discord : boutons alignés dans embed
- [ ] Telegram : menus pour annuler commandes

### ⚡ **Optimisations bienvenues**
- [ ] Discord : enregistrer username_userid dans fichier commande
- [ ] JSON : `command_etat` en chaîne plutôt que nombre
- [ ] Telegram : optimiser fonction `bouton_click`

## 🚨 Points d'attention

### Sécurité
- Ne jamais commiter de vrais tokens
- Utiliser des bots de test pour le développement
- Valider les inputs utilisateur

### Architecture
- Respecter le principe "aucune instance sans sauvegarde JSON"
- Utiliser `command_etat` pour la synchronisation inter-bots
- Préserver l'isolation des threads Discord/Telegram

### Compatibilité
- Tester avec Python 3.8+
- Vérifier l'encodage UTF-8 des fichiers JSON
- S'assurer que les chemins fonctionnent sur Windows/Linux/Mac

## 📞 Besoin d'aide ?

- 🐛 **Bug ou question technique** : Ouvrez une issue GitHub
- 💬 **Discussion générale** : Utilisez les Discussions GitHub
- 📧 **Contact direct** : Voir les contacts dans le README

## 🏆 Reconnaissance

Tous les contributeurs sont ajoutés au README.md avec leurs contributions. Merci de faire grandir ce projet !

---

En contribuant, vous acceptez que votre code soit distribué sous la licence MIT du projet.
