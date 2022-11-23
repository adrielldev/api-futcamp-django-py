from django.urls import path
from . import views

urlpatterns = [
    path("coachs/", views.CreateListCoachView.as_view()),
    path("coachs/<str:coach_id>/", views.GetUpdateDeleteCoachView.as_view()),
]
