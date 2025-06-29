# airport/utils.py
def make_email_body(name: str, dest_list: list[str]) -> str:
    """
    Construit le corps du mail de recommandation.
    dest_list = ["DEL", "ZRH", "LIS"]  → 3 suggestions max.
    """
    if not dest_list:
        return ""

    lignes = [
        f"Bonjour {name} 👋,",
        "",
        "Voici nos destinations personnalisées que vous pourriez aimer :",
        *[f"• {d}" for d in dest_list],
        "",
        "Réservez-les directement sur votre espace passager ✈️",
        "",
        "À très bientôt dans les airs,",
        "L’équipe de l’aéroport Charles de Gaulle ✨",
    ]
    return "\n".join(lignes)
