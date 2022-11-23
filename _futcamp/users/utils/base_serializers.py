from rest_framework import serializers

from teams.models import Team
from coachs.models import Coach
from players.models import Player
from stadiums.models import Stadium
from championships.models import Championship


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
        ]


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
        )

    def get_number_of_titles(self, obj: Player) -> int:
        return obj.titles.all().count()


class CoachSerializer(serializers.ModelSerializer):
    number_of_titles = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = (
            "id",
            "name",
            "birthdate",
            "number_of_titles",
            "hometown",
        )

    def get_number_of_titles(self, obj: Coach) -> int:
        return obj.titles.all().count()


class TeamSerializer(serializers.ModelSerializer):
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

    def get_number_of_titles(self, obj: Player) -> int:
        return obj.titles.all().count()


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
