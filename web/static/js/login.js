/* static/js/login.js */

console.log("Script login.js chargé !");

document.addEventListener('DOMContentLoaded', function () {
    // We bind events here if needed, but onclick handlers are likely in HTML.
    // Ideally we remove onclick from HTML but for now let's just make the functions globally available 
    // and updated for Tailwind.
    showLogin();
});

function updateTabStyles(activeId, inactiveId) {
    const activeTab = document.getElementById(activeId);
    const inactiveTab = document.getElementById(inactiveId);

    if (!activeTab || !inactiveTab) return;

    // Active Style (Tailwind)
    // Original: block py-2 text-primary border-b-2 border-primary font-bold cursor-pointer transition-colors duration-300
    activeTab.className = "block py-2 text-blue-600 border-b-2 border-blue-600 font-bold cursor-pointer transition-colors duration-300";

    // Inactive Style (Tailwind)
    // Original: block py-2 text-gray-500 dark:text-gray-400 border-b-2 border-transparent font-medium cursor-pointer transition-colors duration-300 hover:text-primary
    inactiveTab.className = "block py-2 text-gray-500 dark:text-gray-400 border-b-2 border-transparent font-medium cursor-pointer transition-colors duration-300 hover:text-blue-600";
}

window.showLogin = function () {
    const mainForm = document.getElementById('mainForm');
    const forgotForm = document.getElementById('forgotForm');
    const authTabs = document.getElementById('authTabs');

    const labelIdentifiant = document.getElementById('label-identifiant');
    const fieldEmail = document.getElementById('field-email');
    const linkForgot = document.getElementById('link-forgot');
    const formAction = document.getElementById('form-action');
    const btnSubmit = document.getElementById('btn-submit');
    const bottomTextLogin = document.getElementById('bottom-text-login');
    const bottomTextRegister = document.getElementById('bottom-text-register');

    if (!mainForm) return;

    // 1. Gestion des Vues (Cacher/Montrer)
    // Tailwind uses display classes usually but style.display works fine and is simpler for toggle
    mainForm.style.display = 'flex';
    forgotForm.style.display = 'none';
    if (authTabs) authTabs.style.visibility = 'visible';

    // 2. Configuration pour LOGIN
    if (formAction) formAction.value = "login";
    if (btnSubmit) btnSubmit.innerText = "Connexion";

    // Le label redevient "Utilisateur / Email"
    if (labelIdentifiant) labelIdentifiant.innerText = "Utilisateur / Email";

    // On cache l'email et on montre le lien oubli
    if (fieldEmail) {
        fieldEmail.style.display = 'none'; // hidden
        // We might need to handle 'required' attribute
        const emailInput = document.querySelector('input[name="email"]');
        if (emailInput) emailInput.required = false;
    }

    if (linkForgot) linkForgot.style.display = 'flex';

    // Textes du bas
    if (bottomTextLogin) bottomTextLogin.style.display = 'block';
    if (bottomTextRegister) bottomTextRegister.style.display = 'none';

    // Onglets styling
    updateTabStyles('tab-login', 'tab-register');
}

window.showRegister = function () {
    const mainForm = document.getElementById('mainForm');
    const forgotForm = document.getElementById('forgotForm');

    const labelIdentifiant = document.getElementById('label-identifiant');
    const fieldEmail = document.getElementById('field-email');
    const linkForgot = document.getElementById('link-forgot');
    const formAction = document.getElementById('form-action');
    const btnSubmit = document.getElementById('btn-submit');
    const bottomTextLogin = document.getElementById('bottom-text-login');
    const bottomTextRegister = document.getElementById('bottom-text-register');

    // 1. Affichage
    mainForm.style.display = 'flex';
    forgotForm.style.display = 'none';

    // 2. Configuration pour INSCRIPTION
    if (formAction) formAction.value = "register";
    if (btnSubmit) btnSubmit.innerText = "S'inscrire";

    // Le label devient "Nom d'utilisateur"
    if (labelIdentifiant) labelIdentifiant.innerText = "Nom d'utilisateur";

    // On affiche l'email
    if (fieldEmail) {
        fieldEmail.style.display = 'block';
        const emailInput = document.querySelector('input[name="email"]');
        if (emailInput) emailInput.required = true;
    }

    // Cache le lien oubli
    if (linkForgot) linkForgot.style.display = 'none';

    // Textes du bas
    if (bottomTextLogin) bottomTextLogin.style.display = 'none';
    if (bottomTextRegister) bottomTextRegister.style.display = 'block';

    // Onglets styling
    updateTabStyles('tab-register', 'tab-login');
}

window.showForgot = function () {
    document.getElementById('mainForm').style.display = 'none';
    document.getElementById('forgotForm').style.display = 'flex'; // Use flex to center content properly
    const tabs = document.getElementById('authTabs');
    if (tabs) tabs.style.visibility = 'hidden';
}

/* Fonction pour l'oeil du mot de passe */
window.togglePassword = function () {
    const passwordInput = document.getElementById('passwordInput');
    const passwordIcon = document.getElementById('passwordIcon');

    if (!passwordInput || !passwordIcon) return;

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        passwordIcon.classList.remove('bi-eye');
        passwordIcon.classList.add('bi-eye-slash');
    } else {
        passwordInput.type = "password";
        passwordIcon.classList.remove('bi-eye-slash');
        passwordIcon.classList.add('bi-eye');
    }
}