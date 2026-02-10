# app/admin_routes.py - VERSION CORRIGÉE (full_name au lieu de fullname)

from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from functools import wraps
from werkzeug.security import check_password_hash
import os

# ✅ Créer le blueprint admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_language():
    """Récupérer la langue"""
    return session.get('language', 'fr')

def admin_required(f):
    """Décorateur pour vérifier si l'utilisateur est admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================
# LOGIN
# ============================================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion admin"""
    from app.translations import get_all_translations
    from app.models import AdminUser
    
    language = get_language()
    translations = get_all_translations(language)
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        print(f"🔍 Tentative de login: {email}")
        
        try:
            # ✅ Importer DEDANS la fonction
            from app.models import AdminUser
            
            # ✅ Query
            admin = AdminUser.query.filter_by(email=email).first()
            
            if not admin:
                print(f"❌ Admin not found: {email}")
                return render_template(
                    'admin/login.html',
                    translations=translations,
                    language=language,
                    error='Identifiants invalides'
                )
            
            if not admin.is_active:
                print(f"❌ Admin inactive: {email}")
                return render_template(
                    'admin/login.html',
                    translations=translations,
                    language=language,
                    error='Compte désactivé'
                )
            
            # ✅ Vérifier password
            if not check_password_hash(admin.password_hash, password):
                print(f"❌ Invalid password: {email}")
                return render_template(
                    'admin/login.html',
                    translations=translations,
                    language=language,
                    error='Identifiants invalides'
                )
            
            # ✅ Success
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            session['admin_role'] = admin.role
            
            print(f"✅ Login réussi pour {email}")
            return redirect(url_for('admin.dashboard'))
        
        except Exception as e:
            print(f"❌ Erreur lors du login: {e}")
            import traceback
            traceback.print_exc()
            
            return render_template(
                'admin/login.html',
                translations=translations,
                language=language,
                error=f"Erreur serveur"
            )
    
    return render_template(
        'admin/login.html',
        translations=translations,
        language=language
    )

# ============================================
# LOGOUT
# ============================================

@admin_bp.route('/logout')
def logout():
    """Déconnexion"""
    session.clear()
    return redirect(url_for('admin.login'))

# ============================================
# DASHBOARD
# ============================================

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Dashboard admin"""
    from app.translations import get_all_translations
    from app.models import PendingVehicleRequest, PendingDepotRequest, Vehicle, Depot
    
    language = get_language()
    translations = get_all_translations(language)
    
    pending_vehicles = PendingVehicleRequest.query.filter_by(status='pending').count()
    pending_depots = PendingDepotRequest.query.filter_by(status='pending').count()
    total_vehicles = Vehicle.query.count()
    total_depots = Depot.query.count()
    
    return render_template(
        'admin/dashboard.html',
        translations=translations,
        language=language,
        pending_vehicles=pending_vehicles,
        pending_depots=pending_depots,
        total_vehicles=total_vehicles,
        total_depots=total_depots
    )

# ============================================
# DEMANDES DE VÉHICULES EN ATTENTE
# ============================================

@admin_bp.route('/pending-vehicles')
@admin_required
def pending_vehicles():
    """Voir les demandes de véhicules en attente"""
    from app.translations import get_all_translations
    from app.models import PendingVehicleRequest
    
    language = get_language()
    translations = get_all_translations(language)
    
    # ✅ UTILISER full_name (avec underscore)
    pending = PendingVehicleRequest.query.filter_by(status='pending').all()
    
    return render_template(
        'admin/pending_vehicles.html',
        translations=translations,
        language=language,
        pending_vehicles=pending
    )

# ============================================
# APPROUVER VÉHICULE
# ============================================

@admin_bp.route('/approve-vehicle/<int:request_id>', methods=['POST'])
@admin_required
def approve_vehicle(request_id):
    """Approuver une demande de véhicule"""
    from app.models import PendingVehicleRequest, Vehicle, db
    
    try:
        pending = PendingVehicleRequest.query.get(request_id)
        
        if not pending:
            return {'error': 'Demande non trouvée'}, 404
        
        # ✅ UTILISER full_name (avec underscore)
        vehicle = Vehicle(
            full_name=pending.full_name,
            email=pending.email,
            phone=pending.phone,
            vehicle_type=pending.vehicle_type,
            brand=pending.brand,
            model=pending.model,
            year=pending.year,
            registration=pending.registration,
            location=pending.location,
            description=pending.description,
            image_filename=pending.image_filename,
            is_available=True
        )
        
        db.session.add(vehicle)
        pending.status = 'approved'
        db.session.commit()
        
        return {'success': True, 'message': '✅ Véhicule approuvé'}
    
    except Exception as e:
        print(f"❌ Erreur approbation véhicule: {e}")
        return {'error': str(e)}, 400

# ============================================
# REJETER VÉHICULE
# ============================================

@admin_bp.route('/reject-vehicle/<int:request_id>', methods=['POST'])
@admin_required
def reject_vehicle(request_id):
    """Rejeter une demande de véhicule"""
    from app.models import PendingVehicleRequest, db
    
    try:
        pending = PendingVehicleRequest.query.get(request_id)
        
        if not pending:
            return {'error': 'Demande non trouvée'}, 404
        
        pending.status = 'rejected'
        db.session.commit()
        
        return {'success': True, 'message': '❌ Véhicule rejeté'}
    
    except Exception as e:
        print(f"❌ Erreur rejet véhicule: {e}")
        return {'error': str(e)}, 400

# ============================================
# DEMANDES DE DÉPÔTS EN ATTENTE
# ============================================

@admin_bp.route('/pending-depots')
@admin_required
def pending_depots():
    """Voir les demandes de dépôts en attente"""
    from app.translations import get_all_translations
    from app.models import PendingDepotRequest
    
    language = get_language()
    translations = get_all_translations(language)
    
    # ✅ UTILISER full_name (avec underscore)
    pending = PendingDepotRequest.query.filter_by(status='pending').all()
    
    return render_template(
        'admin/pending_depots.html',
        translations=translations,
        language=language,
        pending_depots=pending
    )

# ============================================
# APPROUVER DÉPÔT
# ============================================

@admin_bp.route('/approve-depot/<int:request_id>', methods=['POST'])
@admin_required
def approve_depot(request_id):
    """Approuver une demande de dépôt"""
    from app.models import PendingDepotRequest, Depot, db
    
    try:
        pending = PendingDepotRequest.query.get(request_id)
        
        if not pending:
            return {'error': 'Demande non trouvée'}, 404
        
        # ✅ UTILISER full_name (avec underscore)
        depot = Depot(
            full_name=pending.full_name,
            email=pending.email,
            phone=pending.phone,
            area=pending.area,
            depot_type=pending.depot_type,
            location=pending.location,
            description=pending.description,
            image_filename=pending.image_filename,
            price_per_month=pending.price_per_month,
            security_deposit=pending.security_deposit,
            is_available=True
        )
        
        db.session.add(depot)
        pending.status = 'approved'
        db.session.commit()
        
        return {'success': True, 'message': '✅ Dépôt approuvé'}
    
    except Exception as e:
        print(f"❌ Erreur approbation dépôt: {e}")
        return {'error': str(e)}, 400

# ============================================
# REJETER DÉPÔT
# ============================================

@admin_bp.route('/reject-depot/<int:request_id>', methods=['POST'])
@admin_required
def reject_depot(request_id):
    """Rejeter une demande de dépôt"""
    from app.models import PendingDepotRequest, db
    
    try:
        pending = PendingDepotRequest.query.get(request_id)
        
        if not pending:
            return {'error': 'Demande non trouvée'}, 404
        
        pending.status = 'rejected'
        db.session.commit()
        
        return {'success': True, 'message': '❌ Dépôt rejeté'}
    
    except Exception as e:
        print(f"❌ Erreur rejet dépôt: {e}")
        return {'error': str(e)}, 400

# ============================================
# GÉRER LES VÉHICULES APPROUVÉS
# ============================================

@admin_bp.route('/vehicles')
@admin_required
def vehicles_page():
    """Gérer les véhicules approuvés"""
    from app.translations import get_all_translations
    from app.models import Vehicle
    
    language = get_language()
    translations = get_all_translations(language)
    
    vehicles = Vehicle.query.all()
    
    return render_template(
        'admin/vehicles.html',
        translations=translations,
        language=language,
        vehicles=vehicles
    )

# ============================================
# GÉRER LES DÉPÔTS APPROUVÉS
# ============================================

@admin_bp.route('/depots')
@admin_required
def depots_page():
    """Gérer les dépôts approuvés"""
    from app.translations import get_all_translations
    from app.models import Depot
    
    language = get_language()
    translations = get_all_translations(language)
    
    depots = Depot.query.all()
    
    return render_template(
        'admin/depots.html',
        translations=translations,
        language=language,
        depots=depots
    )

# ============================================
# SUPPRIMER VÉHICULE
# ============================================

@admin_bp.route('/delete-vehicle/<int:vehicle_id>', methods=['POST'])
@admin_required
def delete_vehicle(vehicle_id):
    """Supprimer un véhicule"""
    from app.models import Vehicle, db
    
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        
        if not vehicle:
            return {'error': 'Véhicule non trouvé'}, 404
        
        db.session.delete(vehicle)
        db.session.commit()
        
        return {'success': True, 'message': '✅ Véhicule supprimé'}
    
    except Exception as e:
        print(f"❌ Erreur suppression véhicule: {e}")
        return {'error': str(e)}, 400

# ============================================
# SUPPRIMER DÉPÔT
# ============================================

@admin_bp.route('/delete-depot/<int:depot_id>', methods=['POST'])
@admin_required
def delete_depot(depot_id):
    """Supprimer un dépôt"""
    from app.models import Depot, db
    
    try:
        depot = Depot.query.get(depot_id)
        
        if not depot:
            return {'error': 'Dépôt non trouvé'}, 404
        
        db.session.delete(depot)
        db.session.commit()
        
        return {'success': True, 'message': '✅ Dépôt supprimé'}
    
    except Exception as e:
        print(f"❌ Erreur suppression dépôt: {e}")
        return {'error': str(e)}, 400

# ============================================
# GÉRER LES COMMENTAIRES
# ============================================

@admin_bp.route('/comments')
@admin_required
def comments():
    """Gérer les commentaires"""
    from app.translations import get_all_translations
    from app.models import Comment
    
    language = get_language()
    translations = get_all_translations(language)
    
    pending_comments = Comment.query.filter_by(status='pending').all()
    
    return render_template(
        'admin/comments.html',
        translations=translations,
        language=language,
        comments=pending_comments
    )

# ============================================
# APPROUVER COMMENTAIRE
# ============================================

@admin_bp.route('/approve-comment/<int:comment_id>', methods=['POST'])
@admin_required
def approve_comment(comment_id):
    """Approuver un commentaire"""
    from app.models import Comment, db
    
    try:
        comment = Comment.query.get(comment_id)
        
        if not comment:
            return {'error': 'Commentaire non trouvé'}, 404
        
        comment.status = 'approved'
        db.session.commit()
        
        return {'success': True, 'message': '✅ Commentaire approuvé'}
    
    except Exception as e:
        print(f"❌ Erreur approbation commentaire: {e}")
        return {'error': str(e)}, 400

# ============================================
# REJETER COMMENTAIRE
# ============================================

@admin_bp.route('/reject-comment/<int:comment_id>', methods=['POST'])
@admin_required
def reject_comment(comment_id):
    """Rejeter un commentaire"""
    from app.models import Comment, db
    
    try:
        comment = Comment.query.get(comment_id)
        
        if not comment:
            return {'error': 'Commentaire non trouvé'}, 404
        
        comment.status = 'rejected'
        db.session.commit()
        
        return {'success': True, 'message': '❌ Commentaire rejeté'}
    
    except Exception as e:
        print(f"❌ Erreur rejet commentaire: {e}")
        return {'error': str(e)}, 400