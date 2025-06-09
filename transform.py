import json
import pandas as pd
import os

def transformer_velib():
    chemin_fichier = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "velib.json"))

    print("[INFO] Chargement du fichier velib.json...")
    with open(chemin_fichier, encoding="utf-8") as f:
        data = json.load(f)

    records = []
    for record in data.get("records", []):
        fields = record.get("fields", {})
        station = {
            "station_id": fields.get("stationcode"),
            "nom": fields.get("name"),
            "etat": fields.get("status"),
            "nb_velos_dispo": fields.get("numbikesavailable", 0),
            "nb_bornes_libres": fields.get("numdocksavailable", 0),
            "mecaniques": fields.get("mechanical", 0),
            "electriques": fields.get("ebike", 0),
            "latitude": fields.get("coordonnees_geo", [None, None])[0],
            "longitude": fields.get("coordonnees_geo", [None, None])[1],
            "mise_a_jour": fields.get("duedate")  # 🕒 nouvelle colonne
        }
        records.append(station)

    df = pd.DataFrame(records)
    print(f"[✅] {len(df)} stations extraites.")

    # Enregistrement CSV
    chemin_sortie = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "velib_clean.csv"))
    df.to_csv(chemin_sortie, index=False)
    print(f"[💾] Données nettoyées sauvegardées dans data/velib_clean.csv")

    return df

if __name__ == "__main__":
    transformer_velib()
