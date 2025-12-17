console.log("Script login.js chargé !");

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
document.addEventListener('DOMContentLoaded', function() {
    console.log("Initialisation du formulaire...");
    showLogin();
});