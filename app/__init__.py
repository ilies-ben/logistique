# app/__init__.py - VERSION OPTIMISÉE POUR VOTRE routes.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# ✅ Instance SQLAlchemy GLOBALE
db = SQLAlchemy()

def create_app():
    """Créer l'application Flask"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    app.config['ITEMS_PER_PAGE'] = 12
    
    # Dossier uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'vehicles'), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'depots'), exist_ok=True)
    
    # ✅ Initialiser SQLAlchemy UNE FOIS
    db.init_app(app)
    
    # ✅ CONTEXTE APP OBLIGATOIRE
    with app.app_context():
        # Importer les modèles
        from app.models import AdminUser, Vehicle, Depot, Comment, PendingVehicleRequest, PendingDepotRequest
        print("✅ Modèles importés avec succès")
        
        # Créer les tables
        db.create_all()
        print("✅ Toutes les tables créées/vérifiées")
        
        # Créer l'admin par défaut
        try:
            admin = AdminUser.query.filter_by(email='admin@plateforme-logistique.com').first()
            if not admin:
                from werkzeug.security import generate_password_hash
                admin = AdminUser(
                    email='admin@plateforme-logistique.com',
                    password_hash=generate_password_hash('admin123456', method='pbkdf2:sha256'),
                    full_name='Administrateur',
                    role='admin',
                    is_active=True
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Compte admin par défaut créé")
            else:
                print("✅ Admin existe déjà")
        except Exception as e:
            print(f"⚠️  Erreur création admin: {e}")
    
    # ✅ Enregistrer les blueprints APRÈS le contexte
    try:
        # ✅ PUBLIC BLUEPRINT (DEPUIS routes.py)
        from app.routes import public_bp
        app.register_blueprint(public_bp)
        print("✅ Blueprint 'public' enregistré depuis routes.py")
    except ImportError as e:
        print(f"❌ Erreur import routes.py: {e}")
    
    try:
        # ✅ ADMIN BLUEPRINT
        from app.admin_routes import admin_bp
        app.register_blueprint(admin_bp)
        print("✅ Blueprint 'admin' enregistré")
    except ImportError as e:
        print(f"⚠️  Erreur admin_routes: {e}")
    
    # ✅ CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    return app


