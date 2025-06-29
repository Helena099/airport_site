# import os, pandas as pd, pymongo, pathlib
# from dotenv import load_dotenv

# BASE = pathlib.Path(__file__).parent   # -> dossier Scripts
# load_dotenv(BASE.parent / ".env")        # charge le .env à la racine

# uri = os.getenv("MONGO_URI")
# assert uri, "MONGO_URI introuvable ! Vérification de .env"

# COL_FILES = {
#     "flights":       BASE / "airport.flights.csv",
#     "passengers":    BASE / "airport.passengers.csv",
#     "services":      BASE / "airport.services.csv",
#     "reservations":  BASE / "airport.reservations.csv",
#     # facultatif
#     # "emails":     BASE / "personalized_emails_sample.csv",
# }

# cli = pymongo.MongoClient(os.getenv("MONGO_URI"))
# db  = cli["airport"]

# for col, path in COL_FILES.items():
#     df = pd.read_csv(path)
#     db[col].delete_many({})          # reset
#     db[col].insert_many(df.to_dict("records"))
#     print(f"{col}: {len(df)} docs")

#!/usr/bin/env python
"""Scripts/load_csv.py – import CSV ➜ Mongo (instrumenté)"""

import os
import pathlib
import pandas as pd
import pymongo
from dotenv import load_dotenv
from datetime import datetime

BASE = pathlib.Path(__file__).parent          # dossier Scripts
ROOT = BASE.parent                            # racine projet

# 1) .env
load_dotenv(ROOT / ".env")
uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
print(f"[{datetime.now():%H:%M:%S}] URI utilisé : {uri}")

# 2) Mongo client
cli = pymongo.MongoClient(uri, serverSelectionTimeoutMS=3000)
try:
    cli.admin.command("ping")
    print("Connexion OK")
except Exception as e:
    print("Impossible de pinger Mongo :", e)
    raise SystemExit(1)

db = cli["airport"]
print("Base ciblée :", db.name)

# 3) CSV à importer  (noms de collections alignés avec Django)
COL_FILES = {
    "airport_flight":       BASE / "airport.flights.csv",
    "airport_passenger":    BASE / "airport.passengers.csv",
    "airport_service":      BASE / "airport.services.csv",
    "airport_reservation":  BASE / "airport.reservations.csv",
}

# 4) Boucle d’import
for col, path in COL_FILES.items():
    print(f"\n[{datetime.now():%H:%M:%S}] {col.upper()} – fichier : {path}")
    if not path.exists():
        print("Fichier introuvable, on skip.")
        continue

    df = pd.read_csv(path)
    print(f"Lignes lues : {len(df)}")

    try:
        db[col].delete_many({})                      # reset
        res = db[col].insert_many(df.to_dict("records"), ordered=False)
        print(f"Insertions   : {len(res.inserted_ids)}")
        print(f"Count après  : {db[col].count_documents({})}")
    except Exception as e:
        print("ERREUR insert_many :", e)

print("\n--- Résumé final ---")
for col in COL_FILES:
    print(f"{col:18s}: {db[col].count_documents({})} docs")
