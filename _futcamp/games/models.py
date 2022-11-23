from django.db import models
import uuid


class Game(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    date = models.DateTimeField()
    result = models.CharField(max_length=150)
    round = models.CharField(max_length=150)

    stadium = models.ForeignKey(
        "stadiums.Stadium",
        on_delete=models.CASCADE,
        related_name="games",
    )
    teams = models.ManyToManyField(
        "teams.Team",
        related_name="games",
    )
    championship = models.ForeignKey(
        "championships.Championship",
        related_name="games",
        on_delete=models.CASCADE,
    )
