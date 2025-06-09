# scripts/extract.py

import requests
import os
import json

def telecharger_donnees_velib():
    url = "https://opendata.paris.fr/api/records/1.0/search/"
    params = {
        "dataset": "velib-disponibilite-en-temps-reel",
        "rows": 1000
    }

    print("[INFO] Téléchargement des données Vélib...")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Sauvegarde dans le dossier data
        dossier_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        os.makedirs(dossier_data, exist_ok=True)

        with open(os.path.join(dossier_data, "velib.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("[✅] Données Vélib sauvegardées dans data/velib.json")
    except Exception as e:
        print(f"[❌ ERREUR] Échec du téléchargement : {e}")

if __name__ == "__main__":
    telecharger_donnees_velib()
