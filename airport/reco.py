# import pandas as pd
# from sklearn.neighbors import NearestNeighbors
# from scipy.sparse import csr_matrix, hstack
# from django.conf import settings
# from pymongo import MongoClient
# from collections import Counter

# # client = MongoClient(settings.DATABASES["default"]["CLIENT"]["host"])
# import os
# client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))

# db = client["airport"]

# def recommend_destinations(passenger_id: str, k: int = 5):
#     df_res = pd.DataFrame(list(db["reservations"].find({}, {"_id": 0})))
#     df_pass = pd.DataFrame(list(db["passengers"].find({}, {"_id": 0})))

#     if df_res.empty or df_pass.empty:
#         return []

#     mat_dest = pd.crosstab(df_res['passenger_id'], df_res['arrival_airport'])
#     mat_class = pd.crosstab(df_pass['passenger_id'], df_pass['travel_class'])

#     commons = sorted(set(mat_dest.index) & set(mat_class.index))
#     if passenger_id not in commons:
#         return []

#     combined = hstack([
#         csr_matrix(mat_dest.loc[commons].values),
#         csr_matrix(mat_class.loc[commons].values)
#     ])

#     knn = NearestNeighbors(metric="cosine").fit(combined)
#     idx = commons.index(passenger_id)
#     dists, idxs = knn.kneighbors(combined[idx], n_neighbors=k+1)

#     neighbours = [commons[i] for i in idxs.flatten()[1:]]
#     seen = set(mat_dest.columns[mat_dest.loc[passenger_id] == 1])

#     suggestions = []
#     for n in neighbours:
#         suggestions += list(set(mat_dest.columns[mat_dest.loc[n] == 1]) - seen)

#     return [d for d, _ in Counter(suggestions).most_common(k)]

"""
Algorithme de recommandation – version robuste
- Supporte l’absence de colonne travel_class
- Lit toujours l’URI définie dans .env (ou localhost)
"""

from collections import Counter
from datetime import datetime

import os
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix, hstack
from pymongo import MongoClient

# connexion Mongo
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
client.admin.command("ping")   # lève une erreur si Mongo n’est pas joignable
db = client["airport"]


def recommend_destinations(passenger_id: str, k: int = 5) -> list[str]:
    """
    Retourne jusqu’à `k` destinations conseillées
    pour le passager `passenger_id`.
    """
    # 1) Charge les deux collections
    df_res = pd.DataFrame(list(db["airport_reservation"].find({}, {"_id": 0})))
    df_pass = pd.DataFrame(list(db["airport_passenger"].find({}, {"_id": 0})))

    if df_res.empty or df_pass.empty:
        return []

    # 2) Matrice destination (un passager × arrival_airport)
    mat_dest = pd.crosstab(df_res["passenger_id"], df_res["arrival_airport"])

    # 3) Matrice classe de voyage – colonne inexistante ⇒ on crée un placeholder
    if "travel_class" not in df_pass.columns:
        df_pass["travel_class"] = "unknown"

    mat_class = pd.crosstab(df_pass["passenger_id"], df_pass["travel_class"])

    # 4) Passagers présents dans les deux matrices
    commons = sorted(set(mat_dest.index) & set(mat_class.index))
    if passenger_id not in commons:
        return []

    # 5) Fusion sparse (destinations + classe)
    combined = hstack([
        csr_matrix(mat_dest.loc[commons].values),
        csr_matrix(mat_class.loc[commons].values),
    ])

    # 6) KNN cosine
    knn = NearestNeighbors(metric="cosine").fit(combined)
    idx_target = commons.index(passenger_id)
    dists, idxs = knn.kneighbors(combined[idx_target], n_neighbors=k + 1)

    neighbours = [commons[i] for i in idxs.flatten()[1:]]  # on ignore soi-même
    already_seen = set(mat_dest.columns[mat_dest.loc[passenger_id] == 1])

    # 7) Suggestions agrégées et triées par fréquence
    suggestions: list[str] = []
    for n in neighbours:
        suggestions += list(set(mat_dest.columns[mat_dest.loc[n] == 1]) - already_seen)

    ranked = [dest for dest, _ in Counter(suggestions).most_common(k)]
    return ranked
