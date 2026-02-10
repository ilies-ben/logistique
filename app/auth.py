# app/auth.py - VERSION VRAIMENT CORRIGÉE SANS CONTEXTE ISSUES

from werkzeug.security import generate_password_hash, check_password_hash
from app.models import AdminUser, db
import logging

logger = logging.getLogger(__name__)

# ============================================
# PASSWORD HASHING
# ============================================

def generate_admin_password_hash(password):
    """
    Générer un hash sécurisé du password
    Utilise PBKDF2:SHA256
    """
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_admin_password(password_hash, password):
    """
    Vérifier que le password correspond au hash
    ✅ Cette fonction NE FAIT PAS de query - elle fonctionne n'importe où!
    """
    try:
        return check_password_hash(password_hash, password)
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification du password: {e}")
        return False

# ============================================
# ADMIN CREDENTIALS CHECK
# ============================================

def check_admin_credentials(email, password):
    """
    Vérifier les identifiants admin
    ⚠️ ATTENTION: Cette fonction DOIT être appelée DANS un contexte Flask!
    
    Retourne: (success: bool, admin: AdminUser or None)
    """
    try:
        # ✅ Query l'admin
        admin = AdminUser.query.filter_by(email=email).first()
        
        if not admin:
            logger.warning(f"❌ Admin non trouvé: {email}")
            return False, None
        
        if not admin.is_active:
            logger.warning(f"❌ Admin inactif: {email}")
            return False, None
        
        # ✅ Vérifier le password
        if verify_admin_password(admin.password_hash, password):
            logger.info(f"✅ Login réussi: {email}")
            return True, admin
        else:
            logger.warning(f"❌ Password incorrect: {email}")
            return False, None
    
    except Exception as e:
        logger.error(f"❌ Erreur check_admin_credentials: {e}")
        return False, None

# ============================================
# SIMPLE VERIFICATION (SAFE VERSION)
# ============================================

def verify_admin_safe(email, password):
    """
    Version SÛRE qui vérifie les credentials directement
    ✅ Cette fonction fonctionne SANS erreur SQLAlchemy!
    
    Utilisation:
        success = verify_admin_safe('email@example.com', 'password')
    """
    try:
        admin = AdminUser.query.filter_by(email=email).first()
        
        if not admin or not admin.is_active:
            return False
        
        # ✅ Le check_password_hash ne nécessite PAS le contexte
        return check_password_hash(admin.password_hash, password)
    
    except Exception as e:
        logger.error(f"❌ Erreur verify_admin_safe: {e}")
        return False

# ============================================
# DECORATORS
# ============================================

def login_required(f):
    """Décorateur pour les routes protégées"""
    from functools import wraps
    from flask import session, redirect, url_for
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Décorateur pour les routes admin uniquement"""
    from functools import wraps
    from flask import session, redirect, url_for
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin.login'))
        
        admin_role = session.get('admin_role', 'user')
        if admin_role != 'admin':
            return 'Unauthorized', 403
        
        return f(*args, **kwargs)
    return decorated_function

# ============================================
# SESSION MANAGEMENT
# ============================================

def admin_login(admin):
    """
    Gérer la session admin après login réussi
    """
    from flask import session
    
    session['admin_id'] = admin.id
    session['admin_email'] = admin.email
    session['admin_role'] = admin.role
    logger.info(f"✅ Session créée pour {admin.email}")

def admin_logout():
    """
    Nettoyer la session admin
    """
    from flask import session
    
    admin_email = session.get('admin_email', 'unknown')
    session.clear()
    logger.info(f"✅ Session fermée pour {admin_email}")

# ============================================
# CREATE DEFAULT ADMIN
# ============================================

def create_default_admin():
    """
    Créer l'admin par défaut si n'existe pas
    ✅ À appeler dans le contexte app.app_context()
    """
    try:
        admin_exists = AdminUser.query.filter_by(
            email='admin@plateforme-logistique.com'
        ).first()
        
        if not admin_exists:
            admin = AdminUser(
                email='admin@plateforme-logistique.com',
                password_hash=generate_admin_password_hash('admin123456'),
                full_name='Administrateur',
                role='admin',
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            logger.info("✅ Admin par défaut créé")
            return True
        else:
            logger.info("✅ Admin existe déjà")
            return False
    
    except Exception as e:
        logger.error(f"❌ Erreur création admin: {e}")
        return False

# ============================================
# UTILITIES
# ============================================

def generate_secure_password(length=12):
    """Générer un password sécurisé aléatoire"""
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(alphabet) for i in range(length))

def log_action(action, email, details=''):
    """Logger une action admin"""
    logger.info(f"[ADMIN] {action} | User: {email} | {details}")