from django.db import models
import uuid


class PositionPlayer(models.TextChoices):
    GOLEIRO = "Goleiro"
    ZAGUEIRO = "Zagueiro"
    LATERAL = "Lateral"
    MEIA = "Meia"
    ATACANTE = "Atacante"
    OTHER = "Jogador"


class Player(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    hometown = models.CharField(max_length=150)
    biography = models.TextField()
    number_of_goals = models.IntegerField()
    position = models.CharField(
        max_length=50,
        choices=PositionPlayer.choices,
        default=PositionPlayer.OTHER,
    )
    shirt_number = models.IntegerField()

    current_team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="players",
        null=True,
        blank=True,
        default=None,
    )
