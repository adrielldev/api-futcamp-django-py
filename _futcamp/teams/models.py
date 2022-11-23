from django.db import models
import uuid


class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    mascot = models.CharField(max_length=150)
    team_foundation_year = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    coach = models.OneToOneField(
        "coachs.Coach",
        on_delete=models.CASCADE,
        related_name="current_team",
        null=True,
        blank=True,
        default=None,
    )
    stadium = models.OneToOneField(
        "stadiums.Stadium",
        on_delete=models.CASCADE,
        related_name="team_owner",
        null=True,
        blank=True,
        default=None,
    )
    championship = models.ForeignKey(
        "championships.Championship",
        on_delete=models.CASCADE,
        related_name="teams",
        null=True,
        blank=True,
        default=None,
    )
