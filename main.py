import os
from dotenv import load_dotenv
from app import create_app, db

# Charger variables d'environnement
load_dotenv()

# Créer l'application
app = create_app()

# Export pour Gunicorn
application = app  # ← RENDERC LE VEUT!

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
