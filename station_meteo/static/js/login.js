console.log("Script login.js chargé !");
/* static/js/login.js */

document.addEventListener('DOMContentLoaded', function () {
    // Récupération des éléments
    const mainForm = document.getElementById('mainForm');
    const forgotForm = document.getElementById('forgotForm');
    const fieldEmail = document.getElementById('field-email');
    const linkForgot = document.getElementById('link-forgot');
    const formAction = document.getElementById('form-action');
    const btnSubmit = document.getElementById('btn-submit');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');
    const tabs = document.getElementById('authTabs');
    const bottomTextLogin = document.getElementById('bottom-text-login');
    const bottomTextRegister = document.getElementById('bottom-text-register');

    // Exposer les fonctions globalement pour les onclick du HTML
    window.showLogin = function () {
        mainForm.style.display = 'flex';
        forgotForm.style.display = 'none';
        tabs.style.visibility = 'visible';

        formAction.value = "login";
        btnSubmit.innerText = "Connexion";

        // Champs
        fieldEmail.style.display = 'none';
        // Note: l'input email est optionnel en mode login
        document.querySelector('input[name="email"]').required = false;
        linkForgot.style.display = 'flex';

        // Textes du bas
        bottomTextLogin.style.display = 'block';
        bottomTextRegister.style.display = 'none';

        // Styles des onglets (via classes CSS)
        tabLogin.classList.add('active-tab');
        tabLogin.classList.remove('text-muted');

        tabRegister.classList.remove('active-tab');
        tabRegister.classList.add('text-muted');
    };

    window.showRegister = function () {
        mainForm.style.display = 'flex';
        forgotForm.style.display = 'none';

        formAction.value = "register";
        btnSubmit.innerText = "S'inscrire";

        // Champs
        fieldEmail.style.display = 'block';
        document.querySelector('input[name="email"]').required = true;
        linkForgot.style.display = 'none';

        // Textes du bas
        bottomTextLogin.style.display = 'none';
        bottomTextRegister.style.display = 'block';

        // Styles des onglets
        tabRegister.classList.add('active-tab');
        tabRegister.classList.remove('text-muted');

        tabLogin.classList.remove('active-tab');
        tabLogin.classList.add('text-muted');
    };

    window.showForgot = function () {
        mainForm.style.display = 'none';
        forgotForm.style.display = 'flex';
        tabs.style.visibility = 'hidden';
    };
});

function showLogin() {
    const mainForm = document.getElementById('mainForm');
    const forgotForm = document.getElementById('forgotForm');
    const authTabs = document.getElementById('authTabs');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    if (!mainForm) return;

    // Affichage
    mainForm.style.display = 'flex';
    forgotForm.style.display = 'none';
    authTabs.style.visibility = 'visible';

    // Contenu
    document.getElementById('form-action').value = "login";
    document.getElementById('btn-submit').innerText = "Connexion";

    // Champs
    document.getElementById('field-email').style.display = 'none';
    document.querySelector('input[name="email"]').required = false;
    document.getElementById('link-forgot').style.display = 'flex';

    // Textes bas
    document.getElementById('bottom-text-login').style.display = 'block';
    document.getElementById('bottom-text-register').style.display = 'none';

    // Onglets (Classes Bootstrap standard + notre CSS)
    tabLogin.classList.add('active');
    tabRegister.classList.remove('active');
}

function showRegister() {
    const mainForm = document.getElementById('mainForm');
    const forgotForm = document.getElementById('forgotForm');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    mainForm.style.display = 'flex';
    forgotForm.style.display = 'none';

    document.getElementById('form-action').value = "register";
    document.getElementById('btn-submit').innerText = "S'inscrire";

    document.getElementById('field-email').style.display = 'block';
    document.querySelector('input[name="email"]').required = true;
    document.getElementById('link-forgot').style.display = 'none';

    document.getElementById('bottom-text-login').style.display = 'none';
    document.getElementById('bottom-text-register').style.display = 'block';

    tabRegister.classList.add('active');
    tabLogin.classList.remove('active');
}

function showForgot() {
    document.getElementById('mainForm').style.display = 'none';
    document.getElementById('forgotForm').style.display = 'flex';
    document.getElementById('authTabs').style.visibility = 'hidden';
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function () {
    console.log("Initialisation du formulaire...");
    showLogin();
});