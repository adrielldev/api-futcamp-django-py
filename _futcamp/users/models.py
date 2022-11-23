from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from .utils import UserManager


class GenreChoices(models.TextChoices):
    MASCULINO = "Masculino"
    FEMININO = "Feminino"
    TRANSGENERO = "Transgênero"
    GENERO_NEUTRO = "Gênero neutro"
    NO_BINARIE = "Não Binário"
    AGENERO = "Agênero"
    PANGENERO = "Pangênero"
    OTHER = "Não informado"


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = None
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    birthdate = models.DateField(null=False)
    genre = models.CharField(
        max_length=560, choices=GenreChoices.choices, default=GenreChoices.OTHER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    favorite_teams = models.ManyToManyField(
        "teams.Team",
        blank=True,
        related_name="users",
    )
    favorite_players = models.ManyToManyField(
        "players.Player",
        blank=True,
        related_name="users",
    )
    favorite_championships = models.ManyToManyField(
        "championships.Championship",
        blank=True,
        related_name="users",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "birthdate"]
