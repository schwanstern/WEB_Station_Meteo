// 1. Récupération des données injectées par Django
// Note : Les IDs 'my-data' et 'my-labels' doivent exister dans le HTML (balises json_script)
const allData = JSON.parse(document.getElementById('my-data').textContent);
const chartLabels = JSON.parse(document.getElementById('my-labels').textContent);

// 2. Configuration (Couleurs + Axe Y préféré)
const configs = {
    'vent': { label: 'Vitesse (km/h)', color: '#0d6efd', axis: 'y' },
    'temp': { label: 'Température (°C)', color: '#e74c3c', axis: 'y' },
    'hum': { label: 'Humidité (%)', color: '#3498db', axis: 'y' },
    'press': { label: 'Pression (hPa)', color: '#2ecc71', axis: 'y1' },
    'lux': { label: 'Luminosité (Lux)', color: '#f1c40f', axis: 'y1' }
};

// 3. État actuel : Quelles mesures sont affichées ? (Vent par défaut)
const activeKeys = new Set(['vent']);

// --- Initialisation Chart.js ---
const ctx = document.getElementById('meteoChart').getContext('2d');
let myChart;

// Récupération dynamique des couleurs du thème Bootstrap
const styles = getComputedStyle(document.body);
const textColor = styles.getPropertyValue('--bs-body-color');
const gridColor = styles.getPropertyValue('--bs-border-color');

function renderChart() {
    if (myChart) myChart.destroy();

    // On construit la liste des datasets en fonction des boutons actifs
    const datasets = [];
    activeKeys.forEach(key => {
        const cfg = configs[key];
        datasets.push({
            label: cfg.label,
            data: allData[key],
            borderColor: cfg.color,
            backgroundColor: cfg.color + '20', // Transparence
            borderWidth: 2,
            tension: 0.4,
            pointRadius: 3,
            yAxisID: cfg.axis,
            fill: false
        });
    });

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartLabels, // Utilise les labels dynamiques
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Valeurs Standard' },
                    grid: { color: gridColor },
                    ticks: { color: textColor }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'Hautes Valeurs (hPa / Lux)' },
                    grid: { drawOnChartArea: false },
                    ticks: { color: textColor }
                },
                x: {
                    grid: { color: gridColor },
                    ticks: { color: textColor }
                }
            },
            plugins: {
                legend: { labels: { color: textColor } }
            }
        }
    });
}

// 4. Fonction Toggle (disponible globalement pour le onclick HTML)
window.toggleData = function (key) {
    const btn = document.getElementById('btn-' + key);

    if (activeKeys.has(key)) {
        activeKeys.delete(key);
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-secondary');
    } else {
        activeKeys.add(key);
        btn.classList.remove('btn-outline-secondary');
        btn.classList.add('btn-primary');
    }

    renderChart();
};

// Démarrage
document.addEventListener('DOMContentLoaded', () => {
    renderChart();
});