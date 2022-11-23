from rest_framework import serializers
from datetime import date

from coachs.models import Coach
from stadiums.models import Stadium
from teams.models import Team
from games.models import Game


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium

        fields = ["id", "name", "description", "localizations"]


class CoachSerializer(serializers.ModelSerializer):
    number_of_titles = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = (
            "id",
            "name",
            "number_of_titles",
            "hometown",
        )

    def get_number_of_titles(self, obj: Coach) -> int:
        return obj.titles.all().count()


class TeamSerializer(serializers.ModelSerializer):
    coach = CoachSerializer(read_only=True)
    stadium = StadiumSerializer(read_only=True)
    number_of_players = serializers.SerializerMethodField()
    number_of_titles = serializers.SerializerMethodField()

    class Meta:
        model = Team

        fields = (
            "id",
            "name",
            "mascot",
            "number_of_players",
            "number_of_titles",
            "team_foundation_year",
            "updated_at",
            "stadium",
            "coach",
        )

    def get_number_of_players(self, obj: Team) -> int:
        return obj.players.all().count()

    def get_number_of_titles(self, obj: Team) -> int:
        return obj.titles.all().count()


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game

        fields = (
            "id",
            "date",
            "stadium",
            "teams",
        )
