import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix, hstack
from django.conf import settings
from pymongo import MongoClient
from collections import Counter

client = MongoClient(settings.DATABASES["default"]["CLIENT"]["host"])
db = client["airport"]

def recommend_destinations(passenger_id: str, k: int = 5):
    df_res = pd.DataFrame(list(db["reservations"].find({}, {"_id": 0})))
    df_pass = pd.DataFrame(list(db["passengers"].find({}, {"_id": 0})))

    if df_res.empty or df_pass.empty:
        return []

    mat_dest = pd.crosstab(df_res['passenger_id'], df_res['arrival_airport'])
    mat_class = pd.crosstab(df_pass['passenger_id'], df_pass['travel_class'])

    commons = sorted(set(mat_dest.index) & set(mat_class.index))
    if passenger_id not in commons:
        return []

    combined = hstack([
        csr_matrix(mat_dest.loc[commons].values),
        csr_matrix(mat_class.loc[commons].values)
    ])

    knn = NearestNeighbors(metric="cosine").fit(combined)
    idx = commons.index(passenger_id)
    dists, idxs = knn.kneighbors(combined[idx], n_neighbors=k+1)

    neighbours = [commons[i] for i in idxs.flatten()[1:]]
    seen = set(mat_dest.columns[mat_dest.loc[passenger_id] == 1])

    suggestions = []
    for n in neighbours:
        suggestions += list(set(mat_dest.columns[mat_dest.loc[n] == 1]) - seen)

    return [d for d, _ in Counter(suggestions).most_common(k)]
