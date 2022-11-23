from django.urls import path

from players.views import PlayerDetailView, PlayerView

urlpatterns = [
    path("players/", PlayerView.as_view()),
    path("players/<player_id>/", PlayerDetailView.as_view()),
]
