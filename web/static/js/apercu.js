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
        needle.style.transform = `rotate(${data.vent_angle}deg)`;
    }

    // 3. Gestion des Jauges (Charts)
    // Couleur vide selon le thème (simplifié, on prend gris clair/foncé selon mode lors de l'init)
    // Pour être parfaitement dynamique si on change de thème sans reload, il faudrait un observer, 
    // mais Chart.js n'est pas réactif au CSS externe facilement sans plugin.
    // On va faire un check initial.

    const isDark = document.documentElement.classList.contains('dark');
    const colorEmpty = isDark ? '#111827' : '#f3f4f6';

    createGauge('tempChart', data.temperature, 50, '#ef4444', colorEmpty);
    createGauge('humChart', data.humidite, 100, '#3b82f6', colorEmpty);
    createGauge('windChart', data.vent_vitesse, 100, '#9ca3af', colorEmpty);
    createGauge('pressChart', data.pression - 900, 150, '#22c55e', colorEmpty);
    createGauge('luxChart', data.luminosite, 1000, '#eab308', colorEmpty);
});

function createGauge(ctxId, value, max, color, colorEmpty) {
    const canvas = document.getElementById(ctxId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const remaining = Math.max(0, max - value);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Valeur", "Reste"],
            datasets: [{
                data: [value, remaining],
                backgroundColor: [color, colorEmpty],
                borderWidth: 0
            }]
        },
        options: {
            rotation: -90,
            circumference: 180,
            cutout: '70%',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}
