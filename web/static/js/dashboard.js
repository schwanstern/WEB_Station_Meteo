// --- Utilitaires Graphiques ---

function getSystemColors() {
    const styles = getComputedStyle(document.body);
    return {
        text: styles.getPropertyValue('--bs-body-color'),
        border: styles.getPropertyValue('--bs-border-color'),
        empty: styles.getPropertyValue('--bs-secondary-bg') || '#eee'
    };
}

// Fonction générique pour créer une jauge
function createGauge(ctxId, value, max, color) {
    const ctx = document.getElementById(ctxId).getContext('2d');
    const remaining = max - value;
    const colors = getSystemColors(); // Récupère les couleurs adaptatives

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Valeur", "Reste"],
            datasets: [{
                data: [value, remaining],
                backgroundColor: [color, colors.empty],
                borderWidth: 0
            }]
        },
        options: {
            rotation: -90, circumference: 180, cutout: '70%',
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: { enabled: false } }
        }
    });
}

// Fonction pour initialiser la boussole
function setCompassAngle(angle) {
    const needle = document.getElementById('needle');
    if (needle) {
        needle.style.transform = `rotate(${angle}deg)`;
    }
}