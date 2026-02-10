class FilterManager {
    constructor() {
        this.currentFilters = {
            vehicle: { type: '', location: '', page: 1 },
            depot: { type: '', location: '', area_min: '', area_max: '', page: 1 }
        };
        this.currentType = 'vehicle';
        this.init();
    }
    
    init() {
        this.initFilterEvents();
        this.initTypeButtons();
    }
    
    initTypeButtons() {
        const vehicleBtn = document.getElementById('type-vehicle');
        const depotBtn = document.getElementById('type-depot');
        
        if (vehicleBtn) {
            vehicleBtn.addEventListener('click', () => {
                this.currentType = 'vehicle';
                this.loadResults('vehicle', 1);
                vehicleBtn.classList.add('active');
                if (depotBtn) depotBtn.classList.remove('active');
            });
        }
        
        if (depotBtn) {
            depotBtn.addEventListener('click', () => {
                this.currentType = 'depot';
                this.loadResults('depot', 1);
                depotBtn.classList.add('active');
                if (vehicleBtn) vehicleBtn.classList.remove('active');
            });
        }
    }
    
    initFilterEvents() {
        // Filtre type de véhicule
        const vehicleTypeFilter = document.getElementById('vehicle-type-filter');
        if (vehicleTypeFilter) {
            vehicleTypeFilter.addEventListener('change', (e) => {
                this.currentFilters.vehicle.type = e.target.value;
                this.loadResults('vehicle', 1);
            });
        }
        
        // Filtre localisation véhicule
        const vehicleLocationFilter = document.getElementById('vehicle-location-filter');
        if (vehicleLocationFilter) {
            vehicleLocationFilter.addEventListener('input', debounce((e) => {
                this.currentFilters.vehicle.location = e.target.value;
                this.loadResults('vehicle', 1);
            }, 300));
        }
        
        // Filtre type de dépôt
        const depotTypeFilter = document.getElementById('depot-type-filter');
        if (depotTypeFilter) {
            depotTypeFilter.addEventListener('change', (e) => {
                this.currentFilters.depot.type = e.target.value;
                this.loadResults('depot', 1);
            });
        }
        
        // Filtre localisation dépôt
        const depotLocationFilter = document.getElementById('depot-location-filter');
        if (depotLocationFilter) {
            depotLocationFilter.addEventListener('input', debounce((e) => {
                this.currentFilters.depot.location = e.target.value;
                this.loadResults('depot', 1);
            }, 300));
        }
        
        // Filtre superficie min
        const areaMinFilter = document.getElementById('area-min-filter');
        if (areaMinFilter) {
            areaMinFilter.addEventListener('change', (e) => {
                this.currentFilters.depot.area_min = e.target.value;
                this.loadResults('depot', 1);
            });
        }
        
        // Filtre superficie max
        const areaMaxFilter = document.getElementById('area-max-filter');
        if (areaMaxFilter) {
            areaMaxFilter.addEventListener('change', (e) => {
                this.currentFilters.depot.area_max = e.target.value;
                this.loadResults('depot', 1);
            });
        }
        
        // Bouton "Appliquer les filtres"
        const applyBtn = document.getElementById('apply-filters');
        if (applyBtn) {
            applyBtn.addEventListener('click', () => {
                this.loadResults(this.currentType, 1);
            });
        }
        
        // Bouton "Effacer les filtres"
        const clearBtn = document.getElementById('clear-filters');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.clearFilters();
            });
        }
    }
    
    loadResults(type, page) {
        const filters = { ...this.currentFilters[type], page };
        const endpoint = type === 'vehicle' ? '/api/vehicles' : '/api/depots';
        
        fetch(`${endpoint}?${new URLSearchParams(filters)}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                this.displayResults(data, type);
                this.updatePagination(data.pages, page, type);
            })
            .catch(error => {
                console.error('Erreur:', error);
                const container = document.getElementById('search-results');
                if (container) {
                    container.innerHTML = '<p class="error">Erreur de chargement. Reessayez.</p>';
                }
            });
    }
    
    displayResults(data, type) {
        const container = document.getElementById('search-results');
        if (!container) return;
        
        const items = type === 'vehicle' ? data.vehicles : data.depots;
        
        container.innerHTML = '';
        
        if (!items || items.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <h3>Aucun resultat trouve</h3>
                    <p>Essayez d\'ajuster vos filtres.</p>
                </div>
            `;
            return;
        }
        
        items.forEach(item => {
            const card = this.createCard(item, type);
            container.appendChild(card);
        });
    }
    
    createCard(item, type) {
        const card = document.createElement('div');
        card.className = 'search-result-card';
        
        if (type === 'vehicle') {
            card.innerHTML = `
                <div class="card-image">
                    <img src="${item.image_url}" alt="${item.brand}">
                </div>
                <div class="card-body">
                    <h3>${item.brand} ${item.model}</h3>
                    <p class="meta">${item.year} - ${item.vehicle_type}</p>
                    <p class="location">${item.location}</p>
                    <div class="rating">
                        <span class="stars">${this.getStars(item.rating)}</span>
                        <span class="count">${item.comments_count} avis</span>
                    </div>
                    <a href="/vehicle/${item.id}" class="btn btn-primary">Voir details</a>
                </div>
            `;
        } else {
            card.innerHTML = `
                <div class="card-image">
                    <img src="${item.image_url}" alt="Depot">
                </div>
                <div class="card-body">
                    <h3>${item.area}m2 - ${item.depot_type === 'with_fridge' ? 'Avec frigo' : 'Sans frigo'}</h3>
                    <p class="location">${item.location}</p>
                    <div class="rating">
                        <span class="stars">${this.getStars(item.rating)}</span>
                        <span class="count">${item.comments_count} avis</span>
                    </div>
                    <a href="/depot/${item.id}" class="btn btn-primary">Voir details</a>
                </div>
            `;
        }
        
        return card;
    }
    
    getStars(rating) {
        const filled = Math.round(rating);
        let stars = '';
        for (let i = 0; i < 5; i++) {
            stars += i < filled ? '★' : '☆';
        }
        return `${stars} ${rating}`;
    }
    
    updatePagination(pages, currentPage, type) {
        const pagination = document.getElementById('pagination');
        if (!pagination) return;
        
        pagination.innerHTML = '';
        
        for (let i = 1; i <= pages; i++) {
            const btn = document.createElement('button');
            btn.textContent = i;
            btn.className = i === currentPage ? 'btn btn-primary' : 'btn btn-outline';
            btn.addEventListener('click', () => this.loadResults(type, i));
            pagination.appendChild(btn);
        }
    }
    
    clearFilters() {
        this.currentFilters[this.currentType] = { page: 1 };
        
        // Réinitialiser les champs
        const inputs = document.querySelectorAll(`[id*="${this.currentType}"]`);
        inputs.forEach(input => {
            if (input.tagName === 'INPUT' || input.tagName === 'SELECT') {
                input.value = '';
            }
        });
        
        this.loadResults(this.currentType, 1);
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialiser
const filterManager = new FilterManager();
window.filterManager = filterManager;
