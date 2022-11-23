from django.db import models
import uuid


class Coach(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    biography = models.CharField(max_length=500)
    hometown = models.CharField(max_length=50)
