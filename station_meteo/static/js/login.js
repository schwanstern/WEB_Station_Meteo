/* static/js/login.js */

console.log("Script login.js chargé !");

document.addEventListener('DOMContentLoaded', function () {
    // On initialise l'affichage correct au chargement
    showLogin();
});

function showLogin() {
    const mainForm = document.getElementById('mainForm');
    const forgotForm = document.getElementById('forgotForm');
    const authTabs = document.getElementById('authTabs');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    // Nouveaux éléments ciblés
    const labelIdentifiant = document.getElementById('label-identifiant');
    const fieldEmail = document.getElementById('field-email');
    const linkForgot = document.getElementById('link-forgot');
    const formAction = document.getElementById('form-action');
    const btnSubmit = document.getElementById('btn-submit');
    const bottomTextLogin = document.getElementById('bottom-text-login');
    const bottomTextRegister = document.getElementById('bottom-text-register');

    if (!mainForm) return;

    // 1. Gestion des Vues (Cacher/Montrer)
    mainForm.style.display = 'flex';
    forgotForm.style.display = 'none';
    authTabs.style.visibility = 'visible';

    // 2. Configuration pour LOGIN
    formAction.value = "login";
    btnSubmit.innerText = "Connexion";

    // Le label redevient "Utilisateur / Email"
    if (labelIdentifiant) labelIdentifiant.innerText = "Utilisateur / Email";

    // On cache l'email et on montre le lien oubli
    fieldEmail.style.display = 'none';
    document.querySelector('input[name="email"]').required = false;
    linkForgot.style.display = 'flex'; // <-- Affiche le bouton oublié

    // Textes du bas
    bottomTextLogin.style.display = 'block';
    bottomTextRegister.style.display = 'none';

    // Onglets
    tabLogin.classList.add('active-tab');
    tabLogin.classList.remove('text-muted');
    tabRegister.classList.remove('active-tab');
    tabRegister.classList.add('text-muted');
}

function showRegister() {
    const mainForm = document.getElementById('mainForm');
    const forgotForm = document.getElementById('forgotForm');

    const labelIdentifiant = document.getElementById('label-identifiant');
    const fieldEmail = document.getElementById('field-email');
    const linkForgot = document.getElementById('link-forgot');
    const formAction = document.getElementById('form-action');
    const btnSubmit = document.getElementById('btn-submit');
    const bottomTextLogin = document.getElementById('bottom-text-login');
    const bottomTextRegister = document.getElementById('bottom-text-register');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    // 1. Affichage
    mainForm.style.display = 'flex';
    forgotForm.style.display = 'none';

    // 2. Configuration pour INSCRIPTION
    formAction.value = "register";
    btnSubmit.innerText = "S'inscrire";

    // Le label devient "Nom d'utilisateur" (Plus clair)
    if (labelIdentifiant) labelIdentifiant.innerText = "Nom d'utilisateur";

    // On affiche l'email et on CACHE le lien oubli
    fieldEmail.style.display = 'block';
    document.querySelector('input[name="email"]').required = true;

    // C'est cette ligne qui cache le bouton "Mot de passe oublié"
    if (linkForgot) linkForgot.style.display = 'none';

    // Textes du bas
    bottomTextLogin.style.display = 'none';
    bottomTextRegister.style.display = 'block';

    // Onglets
    tabRegister.classList.add('active-tab');
    tabRegister.classList.remove('text-muted');
    tabLogin.classList.remove('active-tab');
    tabLogin.classList.add('text-muted');
}

function showForgot() {
    document.getElementById('mainForm').style.display = 'none';
    document.getElementById('forgotForm').style.display = 'flex';
    document.getElementById('authTabs').style.visibility = 'hidden';
}

/* Fonction pour l'oeil du mot de passe */
function togglePassword() {
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