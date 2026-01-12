/**
 * apercu.js
 * Gère les graphiques Chart.js et la boussole pour la page apercu.html
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Récupération des données depuis les data-attributes
    const dataContainer = document.getElementById('apercu-data');
    if (!dataContainer) return;

    const data = {
        temperature: parseFloat(dataContainer.dataset.temperature),
        humidite: parseFloat(dataContainer.dataset.humidite),
        vent_vitesse: parseFloat(dataContainer.dataset.ventVitesse),
        vent_angle: parseFloat(dataContainer.dataset.ventAngle),
        pression: parseFloat(dataContainer.dataset.pression),
        luminosite: parseFloat(dataContainer.dataset.luminosite)
    };

    // 2. Gestion de la Boussole
    const needle = document.getElementById('needle');
    if (needle) {
        // Validation basique pour éviter NaN
        const angle = isNaN(data.vent_angle) ? 0 : data.vent_angle;
        needle.style.transform = `rotate(${angle}deg)`;
    }

    // 3. Gestion des Jauges (Charts)
    // Récupération dynamique des couleurs définies dans style.css
    const styles = getComputedStyle(document.body);
    const colors = {
        temp: styles.getPropertyValue('--chart-temp').trim() || '#ef4444',
        hum: styles.getPropertyValue('--chart-hum').trim() || '#3b82f6',
        wind: styles.getPropertyValue('--chart-wind').trim() || '#9ca3af',
        press: styles.getPropertyValue('--chart-press').trim() || '#10b981',
        lux: styles.getPropertyValue('--chart-lux').trim() || '#eab308',
        emptyLight: styles.getPropertyValue('--chart-empty-light').trim() || 'rgba(0,0,0,0.1)',
    };

    // Fonction helper pour déterminer la couleur de fond "vide" selon le thème
    const emptyColor = colors.emptyLight;

    // Valeurs safe (0 si NaN)
    const val = (v) => isNaN(v) ? 0 : v;

    createGauge('tempChart', val(data.temperature), 50, colors.temp, emptyColor);
    createGauge('humChart', val(data.humidite), 100, colors.hum, emptyColor);
    createGauge('windChart', val(data.vent_vitesse), 100, colors.wind, emptyColor);

    // Pression standard ~1013. On affiche l'écart vs 900 pour visibilité
    const pressVal = Math.max(0, val(data.pression) - 900);
    createGauge('pressChart', pressVal, 150, colors.press, emptyColor);

    // Lux échelle 1000
    createGauge('luxChart', val(data.luminosite), 1000, colors.lux, emptyColor);
});

function createGauge(ctxId, value, max, color, colorEmpty) {
    const canvas = document.getElementById(ctxId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const safeValue = Math.max(0, Math.min(value, max)); // Clamp
    const remaining = max - safeValue;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Valeur", "Vide"],
            datasets: [{
                data: [safeValue, remaining],
                backgroundColor: [color, colorEmpty],
                borderWidth: 0,
                borderRadius: 20, // Bords arrondis modernes
                offset: 0
            }]
        },
        options: {
            rotation: -90,
            circumference: 180,
            cutout: '85%', // Anneau fin
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                animateScale: true,
                animateRotate: true
            },
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}
