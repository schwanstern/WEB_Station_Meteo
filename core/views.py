from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from core import services, forms


def root(request):
    if request.user.is_authenticated:
        return redirect("accueil")
    else:
        return redirect("login")


def login_view(request):
    # Initialize forms with None (unbound) by default
    login_form = forms.LoginForm()
    register_form = forms.RegisterForm()
    
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "login":
            login_form = forms.LoginForm(request.POST)
            if login_form.is_valid():
                identifiant = login_form.cleaned_data['identifiant']
                password = login_form.cleaned_data['mdp']
                
                # Email login logic
                if "@" in identifiant:
                    try:
                        user_obj = User.objects.get(email=identifiant)
                        username_to_login = user_obj.username
                    except User.DoesNotExist:
                        username_to_login = identifiant # Let authenticate fail
                else:
                    username_to_login = identifiant

                user = authenticate(request, username=username_to_login, password=password)

                if user is not None:
                    login(request, user)
                    return redirect("accueil")
                else:
                    messages.error(request, "Email/Utilisateur ou mot de passe incorrect")
            else:
                 # If form is invalid, errors will be in login_form.errors
                 # We can add them to messages if we want to keep the current UI behavior which uses messages
                 # But sticking to standard form handling is better if the template supported it.
                 # The current template shows messages. So let's push a generic error or specific ones.
                 messages.error(request, "Veuillez vérifier vos identifiants.")

        elif action == "register":
            register_form = forms.RegisterForm(request.POST)
            if register_form.is_valid():
                User.objects.create_user(
                    username=register_form.cleaned_data['identifiant'],
                    email=register_form.cleaned_data['email'],
                    password=register_form.cleaned_data['mdp']
                )
                messages.success(request, "Compte créé avec succès ! Connectez-vous.")
            else:
                for field, errors in register_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
    
    return render(request, "login.html", {
        "login_form": login_form,
        "register_form": register_form
    })


def accueil(request):
    mes_alertes = services.get_alerts_logic()
    context = {"time": datetime.now().strftime("%H:%M"), "alerts": mes_alertes}
    return render(request, "index.html", context)


def gestion(request):
    if request.method == "POST":
        form = forms.UpdateSystemForm(request.POST)
        if form.is_valid():
             if services.update_system():
                 messages.success(request, "Mise à jour effectuée avec succès !")
    
    # We pass the state to the template
    return render(request, "gestion.html", {"state": services.get_system_state()})


def apercu(request):
    return render(request, "apercu.html", {"data": services.get_sensor_data()})


def graph(request):
    period = request.GET.get("period", "1h")
    data = services.get_historical_data(period=period)
    
    context = {
        "datasets": data["datasets"],
        "labels": data["labels"],
        "current_period": period,
        "period_label": data["period_label"],
    }

    return render(request, "graph.html", context)


def settings(request):
    return render(request, "settings.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("login")
