# routes.py - Routes publiques de l'application
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from app.models import db, Vehicle, Depot, Comment, PendingVehicleRequest, PendingDepotRequest
from app.translations import get_all_translations, get_translation

# Créer blueprint pour les routes publiques
public_bp = Blueprint('public', __name__)

def allowed_file(filename):
    """Vérifier si le fichier est autorisé"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_language():
    """Récupérer la langue depuis les paramètres ou la session"""
    return request.args.get('lang') or session.get('language', 'fr')

def set_language(lang):
    """Définir la langue"""
    if lang in ['fr', 'en']:
        session['language'] = lang

# ============================================
# PAGE D'ACCUEIL
# ============================================

@public_bp.route('/')
def index():
    """Page d'accueil"""
    language = get_language()
    set_language(language)
    translations = get_all_translations(language)
    
    return render_template('index.html',
                         translations=translations,
                         language=language)

# ============================================
# PAGE DE RECHERCHE
# ============================================

@public_bp.route('/search')
def search():
    """Page de recherche des véhicules et dépôts"""
    language = get_language()
    set_language(language)
    translations = get_all_translations(language)
    search_type = request.args.get('type', 'vehicle')
    
    return render_template('search.html',
                         translations=translations,
                         language=language,
                         search_type=search_type)

# ============================================
# API: RÉCUPÉRER LES VÉHICULES
# ============================================

@public_bp.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """API pour récupérer les véhicules avec filtres"""
    page = request.args.get('page', 1, type=int)
    vehicle_type = request.args.get('vehicle_type', '').strip()
    location = request.args.get('location', '').strip()
    
    # Construire la requête
    query = Vehicle.query.filter_by(is_available=True)
    
    if vehicle_type:
        query = query.filter_by(vehicle_type=vehicle_type)
    if location:
        query = query.filter(Vehicle.location.ilike(f'%{location}%'))
    
    # Pagination
    pagination = query.paginate(page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    
    vehicles = [
        {
            'id': v.id,
            'brand': v.brand,
            'model': v.model,
            'year': v.year,
            'vehicle_type': v.vehicle_type,
            'location': v.location,
            'phone': v.phone,
            'image_url': v.get_image_url(),
            'rating': round(v.get_average_rating(), 1),
            'comments_count': len([c for c in v.comments if c.status == 'approved'])
        }
        for v in pagination.items
    ]
    
    return jsonify({
        'vehicles': vehicles,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

# ============================================
# API: RÉCUPÉRER LES DÉPÔTS
# ============================================

@public_bp.route('/api/depots', methods=['GET'])
def get_depots():
    """API pour récupérer les dépôts avec filtres"""
    page = request.args.get('page', 1, type=int)
    depot_type = request.args.get('depot_type', '').strip()
    location = request.args.get('location', '').strip()
    area_min = request.args.get('area_min', '', type=float)
    area_max = request.args.get('area_max', '', type=float)
    
    # Construire la requête
    query = Depot.query.filter_by(is_available=True)
    
    if depot_type:
        query = query.filter_by(depot_type=depot_type)
    if location:
        query = query.filter(Depot.location.ilike(f'%{location}%'))
    if area_min:
        query = query.filter(Depot.area >= area_min)
    if area_max:
        query = query.filter(Depot.area <= area_max)
    
    # Pagination
    pagination = query.paginate(page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    
    depots = [
        {
            'id': d.id,
            'area': d.area,
            'depot_type': d.depot_type,
            'location': d.location,
            'phone': d.phone,
            'price_per_month': d.price_per_month,
            'image_url': d.get_image_url(),
            'rating': round(d.get_average_rating(), 1),
            'comments_count': len([c for c in d.comments if c.status == 'approved'])
        }
        for d in pagination.items
    ]
    
    return jsonify({
        'depots': depots,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

# ============================================
# DÉTAILS VÉHICULE
# ============================================

@public_bp.route('/vehicle/<int:vehicle_id>')
def vehicle_detail(vehicle_id):
    """Afficher le détail d'un véhicule"""
    language = get_language()
    set_language(language)
    translations = get_all_translations(language)
    
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    approved_comments = [c for c in vehicle.comments if c.status == 'approved']
    
    return render_template('vehicle_detail.html',
                         vehicle=vehicle,
                         comments=approved_comments,
                         translations=translations,
                         language=language)

# ============================================
# DÉTAILS DÉPÔT
# ============================================

@public_bp.route('/depot/<int:depot_id>')
def depot_detail(depot_id):
    """Afficher le détail d'un dépôt"""
    language = get_language()
    set_language(language)
    translations = get_all_translations(language)
    
    depot = Depot.query.get_or_404(depot_id)
    approved_comments = [c for c in depot.comments if c.status == 'approved']
    
    return render_template('depot_detail.html',
                         depot=depot,
                         comments=approved_comments,
                         translations=translations,
                         language=language)

# ============================================
# REJOINDRE LA PLATEFORME
# ============================================

@public_bp.route('/join')
def join():
    """Choix entre ajouter un véhicule ou un dépôt"""
    language = get_language()
    set_language(language)
    translations = get_all_translations(language)
    
    return render_template('join.html',
                         translations=translations,
                         language=language)

# ============================================
# AJOUTER UN VÉHICULE
# ============================================

@public_bp.route('/join/vehicle', methods=['GET', 'POST'])
def join_vehicle():
    """Formulaire pour ajouter un véhicule"""
    language = get_language()
    set_language(language)
    translations = get_all_translations(language)
    
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            vehicle_type = request.form.get('vehicle_type')
            brand = request.form.get('brand')
            model = request.form.get('model')
            year = request.form.get('year', type=int)
            registration = request.form.get('registration')
            location = request.form.get('location')
            description = request.form.get('description')
            
            # Valider les données
            if not all([full_name, email, phone, vehicle_type, brand, model, year, registration, location, description]):
                return render_template('join_vehicle.html',
                                     translations=translations,
                                     language=language,
                                     error='Tous les champs sont obligatoires')
            
            # Traitement de l'image
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.utcnow().timestamp()}_{filename}"
                    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'vehicles')
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    image_filename = filename
            
            # Vérifier si le matricule existe déjà
            if PendingVehicleRequest.query.filter_by(registration=registration).first() or \
               Vehicle.query.filter_by(registration=registration).first():
                return render_template('join_vehicle.html',
                                     translations=translations,
                                     language=language,
                                     error='Ce matricule existe déjà')
            
            # Créer la demande
            pending_request = PendingVehicleRequest(
                full_name=full_name,
                email=email,
                phone=phone,
                vehicle_type=vehicle_type,
                brand=brand,
                model=model,
                year=year,
                registration=registration,
                location=location,
                image_filename=image_filename,
                description=description,
                status='pending'
            )
            
            db.session.add(pending_request)
            db.session.commit()
            
            return render_template('join_vehicle.html',
                                 translations=translations,
                                 language=language,
                                 success=True,
                                 message='✅ Votre demande a été envoyée avec succès. Elle sera examinée par notre équipe.')
        
        except Exception as e:
            return render_template('join_vehicle.html',
                                 translations=translations,
                                 language=language,
                                 error=f'Erreur: {str(e)}')
    
    return render_template('join_vehicle.html',
                         translations=translations,
                         language=language)

# ============================================
# AJOUTER UN DÉPÔT
# ============================================

@public_bp.route('/join/depot', methods=['GET', 'POST'])
def join_depot():
    """Formulaire pour ajouter un dépôt"""
    language = get_language()
    set_language(language)
    translations = get_all_translations(language)
    
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            area = request.form.get('area', type=float)
            depot_type = request.form.get('depot_type')
            location = request.form.get('location')
            description = request.form.get('description')
            price_per_month = request.form.get('price_per_month', type=float)
            security_deposit = request.form.get('security_deposit', type=float)
            
            # Valider les données
            if not all([full_name, email, phone, area, depot_type, location, description]):
                return render_template('join_depot.html',
                                     translations=translations,
                                     language=language,
                                     error='Tous les champs obligatoires doivent être remplis')
            
            # Traitement de l'image
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.utcnow().timestamp()}_{filename}"
                    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'depots')
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    image_filename = filename
            
            # Créer la demande
            pending_request = PendingDepotRequest(
                full_name=full_name,
                email=email,
                phone=phone,
                area=area,
                depot_type=depot_type,
                location=location,
                image_filename=image_filename,
                description=description,
                status='pending'
            )
            
            db.session.add(pending_request)
            db.session.commit()
            
            return render_template('join_depot.html',
                                 translations=translations,
                                 language=language,
                                 success=True,
                                 message='✅ Votre demande a été envoyée avec succès. Elle sera examinée par notre équipe.')
        
        except Exception as e:
            return render_template('join_depot.html',
                                 translations=translations,
                                 language=language,
                                 error=f'Erreur: {str(e)}')
    
    return render_template('join_depot.html',
                         translations=translations,
                         language=language)

# ============================================
# COMMENTAIRES
# ============================================

@public_bp.route('/api/add-comment', methods=['POST'])
def add_comment():
    """Ajouter un commentaire"""
    try:
        data = request.get_json()
        
        vehicle_id = data.get('vehicle_id')
        depot_id = data.get('depot_id')
        rating = data.get('rating', type=int)
        text = data.get('text', '').strip()
        author_phone = data.get('phone', '').strip()
        author_name = data.get('author_name', 'Anonyme').strip()
        
        # Valider les données
        if not (vehicle_id or depot_id) or not rating or not text or not author_phone:
            return jsonify({'error': 'Données manquantes'}), 400
        
        if rating < 1 or rating > 5:
            return jsonify({'error': 'La note doit être entre 1 et 5'}), 400
        
        if len(text) < 10:
            return jsonify({'error': 'Le commentaire doit contenir au moins 10 caractères'}), 400
        
        # Créer le commentaire
        comment = Comment(
            vehicle_id=vehicle_id if vehicle_id else None,
            depot_id=depot_id if depot_id else None,
            rating=rating,
            text=text,
            author_phone=author_phone,
            author_name=author_name,
            status='pending'
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '✅ Commentaire envoyé pour validation'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================
# GESTION DE LA LANGUE
# ============================================

@public_bp.route('/set-language/<lang>')
def set_lang(lang):
    """Changer la langue"""
    set_language(lang)
    return redirect(request.referrer or '/')

# ============================================
# PAGES D'ERREUR
# ============================================

@public_bp.route('/error')
def error_page():
    """Page d'erreur"""
    language = get_language()
    translations = get_all_translations(language)
    message = request.args.get('message', 'Une erreur s\'est produite')
    
    return render_template('error.html',
                         message=message,
                         translations=translations,
                         language=language), 404

@public_bp.errorhandler(404)
def page_not_found(error):
    """Gérer les pages non trouvées"""
    language = get_language()
    translations = get_all_translations(language)
    
    return render_template('error.html',
                         message='Page non trouvée',
                         translations=translations,
                         language=language), 404

@public_bp.errorhandler(500)
def internal_error(error):
    """Gérer les erreurs internes"""
    language = get_language()
    translations = get_all_translations(language)
    
    return render_template('error.html',
                         message='Erreur serveur',
                         translations=translations,
                         language=language), 500