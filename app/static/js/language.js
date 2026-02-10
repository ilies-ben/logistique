/**
 * language.js - Gestion du changement de langue
 * Système multilingue FR/EN
 */

class LanguageManager {
    constructor() {
        this.currentLang = this.getCurrentLanguage();
        this.init();
    }
    
    getCurrentLanguage() {
        // Priorité: URL param > Session > LocalStorage > Default FR
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get('lang');
        
        if (urlLang && (urlLang === 'fr' || urlLang === 'en')) {
            this.setLanguage(urlLang);
            return urlLang;
        }
        
        const sessionLang = sessionStorage.getItem('language');
        if (sessionLang) {
            return sessionLang;
        }
        
        const localLang = localStorage.getItem('language');
        if (localLang) {
            return localLang;
        }
        
        return 'fr';
    }
    
    init() {
        // Écouteurs sur les liens de langue
        const langLinks = document.querySelectorAll('.lang-link');
        langLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const lang = e.currentTarget.dataset.lang || e.currentTarget.textContent.toLowerCase();
                this.changeLanguage(lang);
            });
        });
        
        // Appliquer la langue actuelle
        this.applyLanguage();
    }
    
    changeLanguage(lang) {
        if (lang !== 'fr' && lang !== 'en') return;
        
        // Mettre à jour le stockage
        this.setLanguage(lang);
        
        // Recharger la page avec nouveau paramètre
        const url = new URL(window.location);
        url.searchParams.set('lang', lang);
        window.location.href = url.toString();
    }
    
    setLanguage(lang) {
        this.currentLang = lang;
        sessionStorage.setItem('language', lang);
        localStorage.setItem('language', lang);
    }
    
    applyLanguage() {
        // Mettre à jour les classes CSS pour la langue active
        document.querySelectorAll('.lang-link').forEach(link => {
            const linkLang = link.dataset.lang || link.textContent.toLowerCase();
            if (linkLang === this.currentLang) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
        
        // Mettre à jour le body pour les styles de langue
        document.body.setAttribute('data-lang', this.currentLang);
        
        // Trigger event personnalisé
        document.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { language: this.currentLang }
        }));
    }
}

// Initialiser le gestionnaire de langue
const langManager = new LanguageManager();

// Écouteur global pour les changements de langue
document.addEventListener('languageChanged', function(e) {
    console.log('🌐 Langue changée:', e.detail.language);
    
    // Actions supplémentaires après changement de langue
    updateDynamicContent(e.detail.language);
});

function updateDynamicContent(lang) {
    // Mettre à jour les placeholders des formulaires
    const inputs = document.querySelectorAll('input[placeholder], textarea[placeholder]');
    inputs.forEach(input => {
        // Logique pour changer les placeholders selon la langue
    });
}
