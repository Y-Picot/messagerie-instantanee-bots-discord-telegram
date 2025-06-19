"""
Classe de base pour la gestion des fichiers JSON.

Cette classe abstraite fournit des méthodes communes pour :
- Charger et sauvegarder des fichiers JSON avec encodage UTF-8
- Manipuler des variables dans les fichiers JSON
- Gérer des listes d'éléments avec des IDs

Architecture :
- Chaque classe héritière définit son propre `filename`
- Les méthodes utilisent `@classmethod` pour éviter l'instanciation
- Gestion d'erreurs intégrée avec messages de debug

Utilisation :
```python
class MonFichier(JsonInherited):
    filename = "chemin/vers/mon_fichier.json"
    id_name = "user_id"  # Nom du champ ID pour les listes
```
"""
import json
from typing import Union, List, Optional

class JsonInherited():
    """
    Classe abstraite pour standardiser la gestion des fichiers JSON.

    Tous les fichiers JSON du projet héritent de cette classe pour
    bénéficier des méthodes communes de lecture/écriture avec
    gestion d'erreurs et encodage UTF-8.
    """
    filename = ""  # Utiliser les class enfants, en suivant le modèle si dessous pour bénéficier des methodes par défault
    id_name = ""   # Nom de votre id

    # Default methods
    @classmethod
    def get_json_file(cls) -> Optional[dict]:
        """
        Charge et retourne le contenu du fichier JSON.

        Returns:
            dict: Contenu du fichier JSON ou None si erreur

        Note: Utilise l'encodage UTF-8 pour supporter les caractères spéciaux
        """
        data = None
        try :
            # print("Why : "+ cls.filename)
            with open(cls.filename, 'r') as file:
                data = json.load(file)
        except :
            print("Le fichier n'existe pas : get_json_file()")

        return data

    @classmethod
    def save_json_file(cls, data) -> bool:
        """
        Sauvegarde les données dans le fichier JSON avec encodage UTF-8.

        Args:
            data: Données à sauvegarder (dict ou list)

        Returns:
            bool: True si succès, False si erreur

        Important: L'encodage UTF-8 est obligatoire pour les caractères spéciaux
        """
        success = False
        try :
            with open(cls.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            success = True
        except :
            print("Le fichier n'existe pas : save_json_file()")
        return success

    # Variables
    @classmethod
    def search_json_variable(cls, variable) -> Optional[Union[int, str, List]]:
        """
        Recherche et retourne la valeur d'une variable dans le JSON.

        Args:
            variable (str): Nom de la variable à rechercher

        Returns:
            Union[int, str, List]: Valeur trouvée ou None si inexistante

        Exemple: search_json_variable("announce_message")
        """
        variable_retrieved = None

        data = cls.get_json_file()

        if data is not None :

            try :
                variable_retrieved = data.get(variable)
            except :
                print("La variable n'existe pas : search_json_variable()")

        return variable_retrieved

    @classmethod
    def set_json_variable(cls, variable, new_data) -> bool:
        """
        Modifie la valeur d'une variable dans le fichier JSON.

        Args:
            variable (str): Nom de la variable à modifier
            new_data: Nouvelle valeur à assigner

        Returns:
            bool: True si succès, False si erreur

        Exemple: set_json_variable("announce_message", "Nouveau message")
        """
        success = False
        data = cls.get_json_file()
        if data is not None :

            data[variable] = new_data
            if cls.save_json_file(data) :
                print("Valeur sauvegarder : set_json_variable()")
                success = True
        return success

    # Listes
    @classmethod
    def get_json_element_from_list(cls, id) -> Optional[List]:
        """
        Recherche un élément dans une liste JSON par son ID.

        Args:
            id: Identifiant de l'élément à rechercher

        Returns:
            List: Élément trouvé ou None si inexistant

        Utilise le champ défini dans `id_name` pour la recherche.
        """
        element_search = None
        data = cls.get_json_file()
        if data is not None :

            for element in data :
                if element[cls.id_name] == id:
                    element_search = element
        return element_search

    @classmethod
    def add_json_element_to_list(cls, element) -> bool:
        """
        Ajoute un nouvel élément à la liste JSON.

        Args:
            element: Élément à ajouter à la liste

        Returns:
            bool: True si succès, False si erreur

        L'élément est ajouté à la fin de la liste existante.
        """
        success = False
        data = cls.get_json_file()
        if data is not None :

            if cls.get_json_element_from_list(element[cls.id_name]) is None :
                data.append(element)
                cls.save_json_file(data)
                success = True
            else :
                print("L'element existe deja.")

        return success

    @classmethod
    def delete_json_element_to_list(cls, id) -> bool:
        """
        Supprime un élément de la liste JSON par son ID.

        Args:
            id: Identifiant de l'élément à supprimer

        Returns:
            bool: True si succès, False si erreur

        Reconstruit la liste sans l'élément à supprimer.
        """
        success = False

        updated_user_list = []
        data = cls.get_json_file()
        if data is not None :

            for user in data :
                if user[cls.id_name] != id:
                    updated_user_list.append(user)
                else :
                    success = True
                    print("Element trouvé et supprimer")

            if not success :
                print("Element introuvable")

            cls.save_json_file(updated_user_list)

        return success

# Modèle pour ajouter pour hériter de la class

# from JsonInherited import JsonInherited

# class Modele(JsonInherited):
    # filename = JSON_PATH + "announce.json"