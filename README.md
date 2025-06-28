# Airport Management & Recommendation System

**Full‑stack Django 5 + MongoDB app** for managing flights, passengers, airport services and generating travel‑destination recommendations.

---
## Features
* Web **CRUD** (Create / Read / Update / Delete) for **Passengers, Flights, Services**  
* **K‑Nearest Neighbours** algorithm suggests new destinations for a passenger (`/reco?passenger_id=...`)  
* Clean **Tailwind CSS** templates + Django admin  
* Runs on **MongoDB Atlas** (or local) through **djongo5**  

---
## Stack
| Layer | Tech |
|-------|------|
| Backend | Python 3.11 · Django 5 |
| Database | MongoDB + djongo5 |
| ML | pandas · scikit‑learn |
| Front | Django templates (Tailwind) |

---
## Project Tree
```
airport_site/
├── manage.py
├── .env                 # secrets (Mongo URI, Django key)
├── requirements.txt
├── Makefile             # venv / migrate / run shortcuts
├── airport_site/        # Django settings
│   ├── settings.py
│   └── ...
└── airport/             # Core app
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── reco.py          # recommendation engine
    └── templates/airport/
        └── ...
```

---
## Quick Start

1. **Clone**
   ```bash
   git clone <repo> && cd airport_site
   ```

2. **Environment**
   ```bash
   cp .env.example .env   # or edit .env
   # inside .env
   # DJANGO_SECRET_KEY=super‑secret-key
   # MONGO_URI=mongodb+srv://user:pwd@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

3. **Install**
   *With proxy ? Add `[global] proxy = http://myproxy:3128` to `pip.conf`.*

   ```bash
   make venv           # or: python -m venv venv && . venv/bin/activate
   ```

4. **Migrations + admin**
   ```bash
   make migrate
   venv/bin/python manage.py createsuperuser
   ```

5. **Run**
   ```bash
   make run
   # http://127.0.0.1:8000            (web UI)
   # http://127.0.0.1:8000/admin      (admin)
   ```

---
## Endpoints (HTML views)

| Method | URL | Purpose |
|--------|-----|---------|
| GET  | `/passengers/` | List passengers |
| GET  | `/passengers/add/` | Passenger form |
| POST | `/passengers/add/` | Create passenger |
| GET/POST | `/passengers/<id>/edit/` | Update passenger |
| POST | `/passengers/<id>/delete/` | Delete passenger |
| _(Same pattern for `/flights/` & `/services/`)_ |
| GET  | `/reco?passenger_id=<pid>` | Destination suggestions |

> **API with Postman ?**  
> These routes accept standard form‑encoded POSTs, so you can hit them with Postman by sending the right fields.  
> For a pure JSON REST API, plug **Django REST Framework** later on.

---