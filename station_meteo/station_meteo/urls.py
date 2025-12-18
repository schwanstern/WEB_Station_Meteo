from django.contrib import admin
from django.urls import path
from core import views  # On importe tes vues depuis le dossier core

urlpatterns = [
    path("admin/", admin.site.urls),
    # Voici la traduction de tes @app.route
    path("", views.root, name="root"),
    path("login/", views.login_view, name="login"),
    path("accueil/", views.accueil, name="accueil"),
    path("gestion/", views.gestion, name="gestion"),
    path("apercu/", views.apercu, name="apercu"),
    path("graph/", views.graph, name="graph"),
    path("settings/", views.settings, name="settings"),
    path("logout/", views.logout_view, name="logout"),
]
