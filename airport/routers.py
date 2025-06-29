class MongoRouter:
    """
    Envoie tous les modèles de l'app 'airport' vers la BDD 'mongo'.
    Le reste (auth, admin, sessions…) reste sur 'default' (SQLite).
    """
    app_label = "airport"

    def db_for_read(self, model, **hints):
        return "mongo" if model._meta.app_label == self.app_label else "default"

    db_for_write = db_for_read
