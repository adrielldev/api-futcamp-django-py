from django.urls import path

from . import views

urlpatterns = [
    path("stadiums/", views.StadiumView.as_view()),
    path("stadiums/<str:stadium_id>/", views.StadiumDetailView.as_view()),
]
