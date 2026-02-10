/**
 * Main.js - Scripts principaux de la plateforme logistique
 * Gestion des interactions globales et utilitaires
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Plateforme Logistique - Scripts chargés');
    
    // Gestion des effets hover sur les boutons
    initButtonEffects();
    
    // Gestion du menu responsive
    initMobileMenu();
    
    // Gestion des formulaires
    initFormValidation();
    
    // Lazy loading des images
    initLazyLoading();
    
    // Gestion des tooltips
    initTooltips();
});

function initButtonEffects() {
    // Effet hover sur tous les boutons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 12px rgba(255, 140, 0, 0.3)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
}

function initMobileMenu() {
    // Menu hamburger pour mobile (si implémenté)
    const hamburger = document.querySelector('.hamburger');
    const nav = document.querySelector('.nav');
    
    if (hamburger && nav) {
        hamburger.addEventListener('click', function() {
            nav.classList.toggle('active');
        });
    }
}

function initFormValidation() {
    // Validation en temps réel des formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearValidation(this);
            });
        });
    });
}

function validateField(field) {
    if (!field.value.trim()) {
        field.style.borderColor = '#dc3545';
        field.style.backgroundColor = '#fff5f5';
        return false;
    } else {
        clearValidation(field);
        return true;
    }
}

function clearValidation(field) {
    field.style.borderColor = '';
    field.style.backgroundColor = '';
}

function initLazyLoading() {
    // Lazy loading pour les images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

function initTooltips() {
    // Tooltips simples pour les icônes
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.dataset.tooltip;
            let tip = document.querySelector('.tooltip');
            if (!tip) {
                tip = document.createElement('div');
                tip.className = 'tooltip';
                document.body.appendChild(tip);
            }
            tip.textContent = tooltipText;
            tip.style.left = (this.offsetLeft + this.offsetWidth + 10) + 'px';
            tip.style.top = this.offsetTop + 'px';
            tip.style.display = 'block';
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tip = document.querySelector('.tooltip');
            if (tip) tip.style.display = 'none';
        });
    });
}

// Fonction utilitaire: Copie du numéro de téléphone
function copyPhone(phone) {
    navigator.clipboard.writeText(phone).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = 'Copié!';
        btn.style.background = '#28a745';
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
        }, 2000);
    });
}

// Export des fonctions globales
window.LogisticsApp = {
    copyPhone: copyPhone,
    validateField: validateField
};
