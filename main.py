import os
from dotenv import load_dotenv
from app import create_app, db

# Charger les variables d'environnement
load_dotenv()

# Créer l'application Flask
app = create_app()

# Contexte pour les commandes CLI
with app.app_context():
    # Créer les tables si elles n'existent pas
    db.create_all()
    print("✅ Base de données initialisée")

if __name__ == '__main__':
    # Mode développement
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )