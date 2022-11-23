from django.urls import path
from . import views

urlpatterns = [
    path("titles/", views.TitleView.as_view()),
    path("titles/<str:title_id>/", views.TitleDetailView.as_view()),
]
