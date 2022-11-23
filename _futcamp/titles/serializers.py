from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Title
from teams.models import Team


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year_of_conquest",
        )


class TitleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year_of_conquest",
            "coach",
            "team",
            "players",
        )

        read_only_fields = ["coach", "players"]

    def create(self, validated_data: dict) -> Title:
        team_id = validated_data.pop("team", False)

        title = Title.objects.create(**validated_data, team=None)

        if bool(team_id):
            team = get_object_or_404(Team, id=team_id)

            players = []
            team.titles.add(title)
            if bool(team.coach):
                team.coach.titles.add(title)

            for player in team.players.all():
                players.append(player)

            title.players.set(players)
            team.save()

        return title

    def update(self, instance: Title, validated_data: dict) -> Title:
        validated_data.pop("team", False)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
