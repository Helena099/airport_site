# Airport Recommendation Demo

This repository is a **Django + MongoDB** proof‑of‑concept that

* stores flight / passenger / service data in MongoDB,
* serves CRUD pages with Django,
* suggests similar destinations to a passenger,
* (optionally) e‑mails these suggestions,
* can be queried by REST/JSON for use in Postman.

---

## 1 · Project tree

```
airport_site/                 ← repo root
├─ .env.example               ← sample environment file
├─ README.md                  ← **you are here**
├─ requirements.txt
├─ Scripts/
│  └─ load_csv.py             ← import CSV files into Mongo
├─ analysis_and_graphics/     ← data exploration
│  └─ traffic_analysis.ipynb  ← notebook of explication
├─ static/                    ← (optional) CSS/JS if exists
├─ manage.py
├─ airport_site/              ← Django project
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
└─ airport/                   ← main app
   └─ models.py               ← Djongo models (PK = ObjectId)
      views.py                ← list views use PyMongo, rest uses Django CBV
      routers.py              ← routes airport models to “mongo” DB
      reco.py                 ← K‑NN recommender
      templates/airport/
      ├─ base.html
      ├─ passenger_list.html
      ├─ flight_list.html
      ├─ service_list.html
      └─ reco.html
```

---

## 2 · Quick‑start (local dev)

```bash
git clone https://github.com/yourname/airport_site.git
cd airport_site

# 1) Python venv
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2) MongoDB
#   a) Atlas : create cluster, get connection string
#   b) Local : `mongod --dbpath /your/data`
cp .env.example .env          # fill MONGO_URI (and EMAIL_… if SMTP)

# 3) Import demo data
python Scripts/load_csv.py

# 4) Run Django
python manage.py runserver
```

Visit:

* `http://127.0.0.1:8000/passengers/` – CRUD passengers  
* `http://127.0.0.1:8000/flights/` – flights  
* `http://127.0.0.1:8000/services/` – services  
* `http://127.0.0.1:8000/reco/?passenger_id=P00001` – recommendations

> **Tip:** mails are printed to the console (backend console).  
> Change `EMAIL_BACKEND` in *settings.py* to use SMTP or file backend.

---

## 3 · Environment variables

| Name | Example | Purpose |
|------|---------|---------|
| `MONGO_URI` | `mongodb://localhost:27017/` | Mongo connection |
| `DJANGO_SECRET_KEY` | `change‑me‑in‑prod` | Django secret |
| `EMAIL_USER` | `bot@gmail.com` | (if SMTP) |
| `EMAIL_PASS` | `…` | (if SMTP) |

---

## 4 · API (for Postman)

The same collections are exposed as read‑only JSON:

```
GET /api/passengers/          # paginated list
GET /api/flights/
GET /api/services/
```

Add or tweak viewsets in `airport/api_views.py`.

---
