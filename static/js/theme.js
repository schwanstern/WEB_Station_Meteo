/**
 * theme.js
 * Gère le basculement Dark/Light mode avec Tailwind CSS.
 * Utilise localStorage pour persister le choix.
 */

// Au chargement ou immédiatement pour éviter le flash
(function () {
    if (localStorage.theme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
})();

function toggleTheme() {
    if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
        localStorage.theme = 'light';
    } else {
        document.documentElement.classList.add('dark');
        localStorage.theme = 'dark';
    }

    // Si on est sur la page settings, on met à jour le switch
    const switchEl = document.getElementById('themeSwitch');
    if (switchEl) {
        switchEl.checked = document.documentElement.classList.contains('dark');
    }
}

// Initialisation du switch settings s'il existe
document.addEventListener('DOMContentLoaded', () => {
    const switchEl = document.getElementById('themeSwitch');
    if (switchEl) {
        switchEl.checked = document.documentElement.classList.contains('dark');
    }
});