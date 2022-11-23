from django.urls import path

from games.views import GameView, GameDetailView

urlpatterns = [
    path("games/", GameView.as_view()),
    path("games/<game_id>/", GameDetailView.as_view()),
]
