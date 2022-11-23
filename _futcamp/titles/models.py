from django.db import models
import uuid


class Title(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    year_of_conquest = models.DateField()

    players = models.ManyToManyField(
        "players.Player",
        related_name="titles",
        blank=True,
    )
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="titles",
        null=True,
        blank=True,
        default=None,
    )
    coach = models.ForeignKey(
        "coachs.Coach",
        on_delete=models.CASCADE,
        related_name="titles",
        null=True,
        blank=True,
        default=None,
    )
