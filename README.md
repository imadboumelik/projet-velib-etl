
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

## Prérequis

- Python 3.9+
- Modules nécessaires :

```bash
pip install streamlit pandas folium plotly streamlit-folium
```

---

## ▶Lancement de l'application

Depuis la racine du projet, exécuter :

```bash
streamlit run scripts/dashboard.py
```

---

## Fonctionnement du pipeline

1. **extract.py** : Récupère les dernières données Vélib via l’API Open Data
2. **transform.py** : Nettoie les données et les transforme en DataFrame + CSV
3. **dashboard.py** : 
   - Rafraîchit automatiquement les données (ETL)
   - Affiche une carte avec filtre
   - Donne accès à des analyses simples et un export CSV

---

## Fonctions clés

- Carte Folium avec code couleur selon statut
- Filtrage par nom ou statut (OPEN / CLOSED)
- Street View par station (intégré dans la popup)
- Graphiques : répartition vélos électriques vs mécaniques
- Top 10 stations avec le plus de vélos disponibles
- Statistiques par statut
- Export CSV des données filtrées

---

## Remarques

- L’ETL est relancé à chaque lancement de l'application → quasi temps réel
---

## Réalisé par

Imad Boumelik – M2 Big Data – 
