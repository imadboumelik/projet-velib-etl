
# Projet ETL Vélib’ – Dashboard Big Data

Ce projet met en œuvre un pipeline **ETL complet** (Extract – Transform – Load) autour des données ouvertes de **Vélib Paris**, avec stockage dans **MongoDB**, et visualisation via **Streamlit + Folium + Plotly**.

## Structure du projet

```
projet_velib_etl/
├── data/                  # Données sources et nettoyées
├── scripts/
│   ├── extract.py         # Extraction depuis l’API Vélib
│   ├── transform.py       # Nettoyage et normalisation
│   ├── load.py            # Insertion dans MongoDB
│   └── dashboard.py       # Interface utilisateur interactive
├── visualisation/         # (optionnel) cartes générées
└── README.md
```

---

## 1. Installation des dépendances

Créer un environnement virtuel et installer les packages requis :

```bash
pip install streamlit pandas plotly folium pymongo streamlit-folium
```

---

## 2. Lancement du dashboard

```bash
streamlit run scripts/dashboard.py
```

L'application :
- Télécharge automatiquement les dernières données Vélib
- Transforme et sauvegarde les données nettoyées
- Affiche un dashboard interactif
- Inclut une carte Folium avec lien Street View
- Propose des filtres et des graphiques dynamiques
- Permet de télécharger un export CSV filtré

---

## 3. Utilisation de MongoDB (script `load.py`)

```python
from pymongo import MongoClient
import pandas as pd
import os

def charger_dans_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["velib_db"]
    collection = db["stations_velib"]

    chemin = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "velib_clean.csv"))
    df = pd.read_csv(chemin)
    collection.delete_many({})
    collection.insert_many(df.to_dict(orient="records"))
    print(f"Insertion réussie de {len(df)} documents.")

if __name__ == "__main__":
    charger_dans_mongodb()
```

> Utiliser ce script pour insérer les données dans une base NoSQL si besoin d’une persistance ou d’un accès externe à la base.

---

## Auteur

Projet réalisé par **Imad Boumelik** – M2 Big Data –
