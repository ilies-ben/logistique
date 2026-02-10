# app/models.py - VERSION CORRIGÉE (COLONNES COMPATIBLES routes.py)

from datetime import datetime
from app import db  # ✅ Importer depuis __init__.py

# ============================================
# ADMIN USER MODEL
# ============================================

class AdminUser(db.Model):
    """Modèle pour les administrateurs"""
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), default='admin', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AdminUser {self.email}>'

# ============================================
# VEHICLE MODEL
# ============================================

class Vehicle(db.Model):
    """Modèle pour les véhicules approuvés"""
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    registration = db.Column(db.String(50), nullable=False, unique=True, index=True)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=0, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    comments = db.relationship('Comment', backref='vehicle', lazy=True, cascade='all, delete-orphan')
    
    def get_image_url(self):
        """Retourner l'URL de l'image"""
        if self.image_filename:
            return f'/uploads/vehicles/{self.image_filename}'
        return '/static/images/default-vehicle.png'
    
    def get_average_rating(self):
        """Calculer la note moyenne"""
        if not self.comments:
            return 0
        approved_comments = [c for c in self.comments if c.status == 'approved']
        if not approved_comments:
            return 0
        return sum(c.rating for c in approved_comments) / len(approved_comments)
    
    def __repr__(self):
        return f'<Vehicle {self.registration}>'

# ============================================
# DEPOT MODEL
# ============================================

class Depot(db.Model):
    """Modèle pour les dépôts approuvés"""
    __tablename__ = 'depots'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    area = db.Column(db.Float, nullable=False)
    depot_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    price_per_month = db.Column(db.Float, nullable=True)
    security_deposit = db.Column(db.Float, nullable=True)
    rating = db.Column(db.Float, default=0, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    comments = db.relationship('Comment', backref='depot', lazy=True, cascade='all, delete-orphan')
    
    def get_image_url(self):
        """Retourner l'URL de l'image"""
        if self.image_filename:
            return f'/uploads/depots/{self.image_filename}'
        return '/static/images/default-depot.png'
    
    def get_average_rating(self):
        """Calculer la note moyenne"""
        if not self.comments:
            return 0
        approved_comments = [c for c in self.comments if c.status == 'approved']
        if not approved_comments:
            return 0
        return sum(c.rating for c in approved_comments) / len(approved_comments)
    
    def __repr__(self):
        return f'<Depot {self.location}>'

# ============================================
# COMMENT MODEL
# ============================================

class Comment(db.Model):
    """Modèle pour les commentaires"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    depot_id = db.Column(db.Integer, db.ForeignKey('depots.id'), nullable=True)
    author_name = db.Column(db.String(120), default='Anonyme', nullable=False)
    author_phone = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment {self.id}>'

# ============================================
# PENDING VEHICLE REQUEST MODEL
# ============================================

class PendingVehicleRequest(db.Model):
    """Modèle pour les demandes de véhicules en attente"""
    __tablename__ = 'pending_vehicle_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    registration = db.Column(db.String(50), nullable=False, unique=True, index=True)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PendingVehicleRequest {self.registration}>'

# ============================================
# PENDING DEPOT REQUEST MODEL
# ============================================

class PendingDepotRequest(db.Model):
    """Modèle pour les demandes de dépôts en attente"""
    __tablename__ = 'pending_depot_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    area = db.Column(db.Float, nullable=False)
    depot_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    price_per_month = db.Column(db.Float, nullable=True)
    security_deposit = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PendingDepotRequest {self.location}>'