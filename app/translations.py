# Traductions multilingues
TRANSLATIONS = {
    'fr': {
        # Navigation et menu
        'home': 'Accueil',
        'vehicles': 'Véhicules',
        'depots': 'Dépôts',
        'contact': 'Nous contacter',
        'join': 'Rejoindre la plateforme',
        'language': 'Langue',
        
        # Page d\'accueil
        'welcome': 'Bienvenue sur la plateforme logistique',
        'find_vehicle': 'Vous cherchez un véhicule pour transport ?',
        'view_vehicles': 'Voir les véhicules',
        'find_depot': 'Vous cherchez un dépôt ?',
        'view_depots': 'Voir les dépôts',
        'what_looking_for': 'Vous cherchez quoi ?',
        'vehicle_option': 'Véhicule pour transport',
        'depot_option': 'Dépôt',
        
        # Formulaire
        'full_name': 'Nom complet',
        'email': 'Email',
        'phone': 'Numéro de téléphone',
        'vehicle_type': 'Type de véhicule',
        'brand': 'Marque',
        'model': 'Modèle',
        'year': 'Année',
        'registration': 'Matricule',
        'location': 'Localisation',
        'image': 'Image principale',
        'description': 'Description',
        'submit': 'Soumettre',
        'cancel': 'Annuler',
        
        # Véhicules
        'light_car': 'Voiture légère (berline/citadine)',
        'light_van': 'Fourgonnette / utilitaire léger',
        'light_truck': 'Camion léger (-5t)',
        'heavy_truck': 'Camion lourd (+5t)',
        'car_carrier': 'Camion porte-voitures',
        
        # Dépôts
        'area_m2': 'Superficie (m²)',
        'depot_type': 'Type de dépôt',
        'with_fridge': 'Avec frigidaire',
        'without_fridge': 'Sans frigidaire',
        
        # Filtres
        'filter': 'Filtrer',
        'area_range': 'Plage de superficie',
        'results': 'résultats',
        'no_results': 'Aucun résultat trouvé',
        
        # Commentaires
        'leave_comment': 'Laisser un commentaire',
        'rating': 'Note',
        'comment': 'Commentaire',
        'show_number': 'Afficher le numéro',
        
        # Admin
        'admin': 'Admin',
        'login': 'Connexion',
        'logout': 'Déconnexion',
        'dashboard': 'Tableau de bord',
        'pending_requests': 'Demandes en attente',
        'approved_vehicles': 'Véhicules approuvés',
        'approved_depots': 'Dépôts approuvés',
        'pending_comments': 'Commentaires en attente',
        'approve': 'Approuver',
        'reject': 'Refuser',
        'edit': 'Modifier',
        'delete': 'Supprimer',
        'view': 'Voir',
        
        # Contact
        'support_email': 'Email support',
        'phone_number': 'Numéro de téléphone',
        'legal_notice': 'Mentions légales',
        
        # Messages
        'success': 'Opération réussie',
        'error': 'Une erreur s\'est produite',
        'invalid_login': 'Identifiants invalides',
        'request_sent': 'Votre demande a été envoyée avec succès',
    },
    'en': {
        # Navigation and menu
        'home': 'Home',
        'vehicles': 'Vehicles',
        'depots': 'Depots',
        'contact': 'Contact Us',
        'join': 'Join the platform',
        'language': 'Language',
        
        # Homepage
        'welcome': 'Welcome to the logistics platform',
        'find_vehicle': 'Looking for a vehicle for transport?',
        'view_vehicles': 'View vehicles',
        'find_depot': 'Looking for a depot?',
        'view_depots': 'View depots',
        'what_looking_for': 'What are you looking for?',
        'vehicle_option': 'Vehicle for transport',
        'depot_option': 'Depot',
        
        # Forms
        'full_name': 'Full Name',
        'email': 'Email',
        'phone': 'Phone Number',
        'vehicle_type': 'Vehicle Type',
        'brand': 'Brand',
        'model': 'Model',
        'year': 'Year',
        'registration': 'Registration Number',
        'location': 'Location',
        'image': 'Main Image',
        'description': 'Description',
        'submit': 'Submit',
        'cancel': 'Cancel',
        
        # Vehicles
        'light_car': 'Light Car (sedan/hatchback)',
        'light_van': 'Light Van / Light Utility',
        'light_truck': 'Light Truck (-5t)',
        'heavy_truck': 'Heavy Truck (+5t)',
        'car_carrier': 'Car Carrier',
        
        # Depots
        'area_m2': 'Area (m²)',
        'depot_type': 'Depot Type',
        'with_fridge': 'With refrigerator',
        'without_fridge': 'Without refrigerator',
        
        # Filters
        'filter': 'Filter',
        'area_range': 'Area Range',
        'results': 'results',
        'no_results': 'No results found',
        
        # Comments
        'leave_comment': 'Leave a comment',
        'rating': 'Rating',
        'comment': 'Comment',
        'show_number': 'Show number',
        
        # Admin
        'admin': 'Admin',
        'login': 'Login',
        'logout': 'Logout',
        'dashboard': 'Dashboard',
        'pending_requests': 'Pending Requests',
        'approved_vehicles': 'Approved Vehicles',
        'approved_depots': 'Approved Depots',
        'pending_comments': 'Pending Comments',
        'approve': 'Approve',
        'reject': 'Reject',
        'edit': 'Edit',
        'delete': 'Delete',
        'view': 'View',
        
        # Contact
        'support_email': 'Support Email',
        'phone_number': 'Phone Number',
        'legal_notice': 'Legal Notice',
        
        # Messages
        'success': 'Operation successful',
        'error': 'An error occurred',
        'invalid_login': 'Invalid credentials',
        'request_sent': 'Your request has been sent successfully',
    }
}

def get_translation(key, language='fr'):
    """Obtenir une traduction"""
    return TRANSLATIONS.get(language, TRANSLATIONS['fr']).get(key, key)

def get_all_translations(language='fr'):
    """Obtenir tous les textes pour une langue"""
    return TRANSLATIONS.get(language, TRANSLATIONS['fr'])
