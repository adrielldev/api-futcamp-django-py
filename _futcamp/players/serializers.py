from rest_framework import serializers
from django.shortcuts import get_object_or_404
from datetime import date

from .models import Player
from teams.models import Team
from .utils import TeamSerializer, TitleSerializer


class PlayerSerializer(serializers.ModelSerializer):
    number_of_goals = serializers.IntegerField(min_value=0)
    number_of_titles = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = (
            "id",
            "name",
            "birthdate",
            "hometown",
            "number_of_goals",
            "number_of_titles",
            "position",
            "shirt_number",
            "current_team",
        )

    def get_number_of_titles(self, obj: Player) -> int:
        return obj.titles.all().count()


class PlayerDetailSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    number_of_titles = serializers.SerializerMethodField()
    number_of_goals = serializers.IntegerField(min_value=0)
    titles = TitleSerializer(many=True, read_only=True)
    current_team = TeamSerializer(read_only=True)

    class Meta:
        model = Player
        fields = (
            "id",
            "name",
            "birthdate",
            "age",
            "hometown",
            "biography",
            "number_of_goals",
            "number_of_titles",
            "titles",
            "position",
            "shirt_number",
            "current_team",
        )

    def get_age(self, obj: Player) -> int:
        current_date = date.today()
        player_birthdate = obj.birthdate

        age = (
            current_date.year
            - player_birthdate.year
            - (
                (current_date.month, current_date.day)
                < (player_birthdate.month, player_birthdate.day)
            )
        )

        return age

    def get_number_of_titles(self, obj: Player) -> int:
        return obj.titles.all().count()

    def create(self, validated_data: dict) -> Player:
        team_id = validated_data.pop("current_team", False)

        player = Player.objects.create(**validated_data)
        if bool(team_id):
            team = get_object_or_404(Team, id=team_id)
            team.players.add(player)
            team.save()

        return player

    def update(self, instance: Player, validated_data: dict) -> Player:
        team_id = validated_data.pop("current_team", False)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if bool(team_id):
            team = get_object_or_404(Team, id=team_id)
            instance.current_team = team

        instance.save()

        return instance
