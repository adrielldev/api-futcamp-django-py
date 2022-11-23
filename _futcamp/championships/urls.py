from django.urls import path
from .views import ChampionshipDetailView, ChampionshipView

urlpatterns = [
    path("championships/", ChampionshipView.as_view()),
    path("championships/<str:championship_id>/", ChampionshipDetailView.as_view()),
]
