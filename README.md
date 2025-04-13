# Cardinal

Cardinal est une API flexible et extensible développée en Python avec FastAPI, permettant d'ajouter, modifier ou supprimer dynamiquement des endpoints API grâce à un système de modules.

## 🌟 Vision

Créer une API modulaire en développement continu où il suffit d'ajouter des fichiers Python pour étendre automatiquement les fonctionnalités, sans interruption de service ni modification du code existant.

## 🔑 Caractéristiques principales

- **Architecture modulaire**: Ajout facile de nouvelles fonctionnalités via des modules indépendants
- **Découverte automatique**: Le core détecte et intègre automatiquement les nouveaux modules
- **Développement continu**: Ajoutez des API à l'infini sans toucher au code existant
- **Documentation auto-générée**: Interface Swagger générée automatiquement pour tous les modules
- **Isolation des modules**: Chaque module peut évoluer indépendamment

## 🏗️ Architecture

Cardinal se compose de deux éléments principaux:

### Core
Le noyau de l'application qui fournit:
- Détection et chargement automatique des modules
- Routage des requêtes vers les modules appropriés
- Gestion des erreurs et logging centralisés
- Configuration globale

### Modules
Des composants indépendants qui:
- S'enregistrent automatiquement auprès du core
- Définissent leurs propres endpoints API
- Implémentent leur logique métier spécifique
- Peuvent être ajoutés/modifiés/supprimés à la volée

## 🚀 Installation

```bash
# Cloner le dépôt
git clone https://github.com/username/cardinal.git
cd cardinal

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## ✨ Création d'un nouveau module

1. Créez un nouveau dossier dans `modules/` (par exemple `modules/my_module/`)
2. Ajoutez les fichiers nécessaires:
   - `__init__.py` - Pour l'auto-découverte
   - `routes.py` - Pour définir vos endpoints
   - `models.py` - Pour les modèles de données Pydantic
   - `services.py` - Pour la logique métier

Exemple de structure d'un module:
```python
# modules/my_module/__init__.py
from .routes import router  # Pour que le module_loader trouve le router

# modules/my_module/routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/my-module", tags=["My Module"])

@router.get("/")
async def read_root():
    return {"message": "Hello from my module!"}
```

Le core détectera automatiquement votre module et ajoutera ses routes à l'API!

## 🧪 Tests

```bash
# Exécuter les tests
pytest
```

## 📘 Documentation

La documentation complète est générée automatiquement et accessible à:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔄 Développement continu

Cardinal est conçu pour un développement continu:
- Ajoutez de nouveaux modules à tout moment
- Modifiez les modules existants
- Le core se charge de les intégrer sans redémarrage

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE)