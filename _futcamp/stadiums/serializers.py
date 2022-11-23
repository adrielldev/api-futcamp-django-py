from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Stadium
from teams.models import Team
from .utils import TeamSerializer


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium

        fields = [
            "id",
            "name",
            "description",
            "capacity",
            "localizations",
            "area",
            "team_owner",
        ]


class StadiumDetailSerializer(serializers.ModelSerializer):
    team_owner = TeamSerializer(read_only=True)

    class Meta:
        model = Stadium

        fields = [
            "id",
            "name",
            "description",
            "capacity",
            "localizations",
            "area",
            "team_owner",
        ]

    def create(self, validated_data: dict) -> Stadium:
        team_id = validated_data.pop("team_owner", False)

        stadium = Stadium.objects.create(**validated_data)
        if bool(team_id):
            team = get_object_or_404(Team, id=team_id)
            team.stadium = stadium

            team.save()

        return stadium

    def update(self, instance: Stadium, validated_data: dict) -> Stadium:
        team_id = validated_data.pop("team_owner", False)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if bool(team_id):
            team = get_object_or_404(Team, id=team_id)
            instance.team_owner = team

        instance.save()

        return instance
