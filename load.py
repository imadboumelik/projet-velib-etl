import pandas as pd
from pymongo import MongoClient
import os

def charger_dans_mongodb():
    # Chargement du fichier nettoyé
    chemin_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "velib_clean.csv"))
    df = pd.read_csv(chemin_csv)

    # Connexion à MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["velib_db"]
    collection = db["stations_velib"]

    # Nettoyage : suppression des anciens documents
    collection.drop()

    # Insertion des documents
    records = df.to_dict(orient="records")
    collection.insert_many(records)

    print(f"[✓] {len(records)} documents insérés dans MongoDB (base: velib_db, collection: stations_velib)")

if __name__ == "__main__":
    charger_dans_mongodb()
