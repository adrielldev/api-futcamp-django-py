from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Championship

from .utils import TeamSerializer, GameSerializer
from teams.models import Team


class ChampionshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship

        fields = (
            "id",
            "name",
            "description",
            "initial_date",
            "end_date",
            "award",
        )


class ChampionshipDetailSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = Championship

        fields = (
            "id",
            "name",
            "description",
            "initial_date",
            "end_date",
            "award",
            "teams",
            "games",
        )

    def create(self, validated_data: dict) -> Championship:
        team_list = validated_data.pop("teams", False)

        championship = Championship.objects.create(**validated_data)

        if bool(team_list):
            for team_id in team_list:
                team = get_object_or_404(Team, id=team_id)
                championship.teams.add(team)

        return championship

    def update(self, instance: Championship, validated_data: dict) -> Championship:
        team_list = validated_data.pop("teams", False)
        championship = Championship.objects.filter(id=instance.id).first()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if bool(team_list):
            championship.teams.clear()

            for team_id in team_list:
                team = get_object_or_404(Team, id=team_id)
                championship.teams.add(team)

        instance.save()

        return instance
