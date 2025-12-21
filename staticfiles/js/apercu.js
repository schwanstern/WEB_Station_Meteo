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

    const styles = getComputedStyle(document.body);
    const isDark = document.documentElement.classList.contains('dark');

    // Récupération dynamique depuis le CSS
    const colorEmpty = isDark ?
        styles.getPropertyValue('--chart-empty-dark').trim() :
        styles.getPropertyValue('--chart-empty-light').trim();

    const colors = {
        temp: styles.getPropertyValue('--chart-temp').trim(),
        hum: styles.getPropertyValue('--chart-hum').trim(),
        wind: styles.getPropertyValue('--chart-wind').trim(),
        press: styles.getPropertyValue('--chart-press').trim(),
        lux: styles.getPropertyValue('--chart-lux').trim()
    };

    // Scaling Logic:
    // Temp: -10 to 40 (Range 50) -> offset +10
    // Hum: 0 to 100
    // Wind: 0 to 100
    // Press: 960 to 1040 (Range 80) -> offset 960
    // Lux: 0 to 1000

    createGauge('tempChart', data.temperature + 10, 50, colors.temp, colorEmpty);
    createGauge('humChart', data.humidite, 100, colors.hum, colorEmpty);
    createGauge('windChart', data.vent_vitesse, 100, colors.wind, colorEmpty);
    createGauge('pressChart', data.pression - 960, 80, colors.press, colorEmpty); // 960hPa min
    createGauge('luxChart', data.luminosite, 2000, colors.lux, colorEmpty);
});

function createGauge(ctxId, value, max, color, colorEmpty) {
    const canvas = document.getElementById(ctxId);
    if (!canvas) return;

    // Clamp value logic
    let displayValue = value;
    if (displayValue < 0) displayValue = 0;
    if (displayValue > max) displayValue = max;

    // Safety check for invalid numbers (prevents chart crash)
    if (isNaN(displayValue)) displayValue = 0;

    const ctx = canvas.getContext('2d');
    const remaining = max - displayValue;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Valeur", "Reste"],
            datasets: [{
                data: [displayValue, remaining],
                backgroundColor: [color, colorEmpty],
                borderWidth: 0,
                // Modern Touch: Rounded Ends
                borderRadius: 20,
                // Space between active and track
                borderJoinStyle: 'round',
                spacing: 2,
            }]
        },
        options: {
            rotation: -90,
            circumference: 180,
            cutout: '80%', // Thinner ring
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
