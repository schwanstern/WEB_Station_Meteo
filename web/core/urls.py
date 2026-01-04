from django.urls import path
from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("login/", views.login_view, name="login"),
    path("accueil/", views.accueil, name="accueil"),
    path("gestion/", views.gestion, name="gestion"),
    path("apercu/", views.apercu, name="apercu"),
    path("graph/", views.graph, name="graph"),
    path("settings/", views.settings, name="settings"),
    path("logout/", views.logout_view, name="logout"),
]
