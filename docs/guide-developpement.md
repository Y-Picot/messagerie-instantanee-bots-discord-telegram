# 🤖 Guide Développement - Bots Discord & Telegram

> 📚 **Nouveau dans le projet ?** Consultez d'abord le [Guide d'Installation](installation.md) pour configurer votre environnement.

## 🏗️ Architecture
**📁 Stockage** : Fichiers JSON uniquement
- Aucune instance sans sauvegarde JSON
- Objets réinstanciés au redémarrage
- Pas d'instances persistantes

**📡 Communication** :
- Discord et Telegram sur threads séparés
- Synchronisation via `command_etat` (0=en cours, 1=annulé, 2=terminé)
- Un plantage n'affecte pas l'autre bot

## 🔧 Solutions Techniques

**Imports circulaires** :
```python
import nom_fichier as nom
# Utilisation : nom.class.fonction
```

**Asynchrone** :
- 🟣 Discord : `async/await` natif
- 🔵 Telegram : système interne, pas besoin d'`async/await`

**Encodage** :
```python
with open(file_path, 'w', encoding='utf-8') as file:
```

## 📋 TODO / Améliorations

### **Options** :
- [ ] 🔧 Main : relance des threads
- [ ] 🟣 Discord : boutons alignés dans embed
- [ ] 🔵 Telegram : menus pour annuler commandes

### **Optimisations** :
- [ ] 🟣 Discord : enregistrer username_userid dans fichier commande
- [ ] 🟣 Discord : nettoyage auto "Commande-annulee"
- [ ] 📁 JSON : `command_etat` en chaîne plutôt que nombre
- [ ] 🔵 Telegram : optimiser fonction `bouton_click`

### **Futures** :
- [ ] 🧪 Tests unitaires boîte noire
- [ ] 🔵 Telegram : délai anti-spam
- [ ] 🟣 Discord : gestion paramètres multiples

## 📝 Notes Utiles

**🟣 Embeds Discord** :
```python
embed.add_field(name="", value="", inline=False)  # inline=False : ligne complète
```

**🔗 Synchronisation** : Utiliser `command_etat` uniquement entre Discord/Telegram, pas en interne
