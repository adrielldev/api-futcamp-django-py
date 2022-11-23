from rest_framework import serializers

from teams.models import Team
from coachs.models import Coach
from players.models import Player


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


class PlayerSerializer(serializers.ModelSerializer):
    number_of_goals = serializers.IntegerField(min_value=0)
    number_of_titles = serializers.SerializerMethodField()

    class Meta:
        model = Player

        fields = (
            "id",
            "name",
            "hometown",
            "number_of_goals",
            "number_of_titles",
            "position",
            "shirt_number",
        )

    def get_number_of_titles(self, obj: Player) -> int:
        return obj.titles.all().count()


class TeamSerializer(serializers.ModelSerializer):
    coach = CoachSerializer(read_only=True)
    players = PlayerSerializer(many=True, read_only=True)
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
            "coach",
            "players",
        )

    def get_number_of_players(self, obj: Team) -> int:
        return obj.players.all().count()

    def get_number_of_titles(self, obj: Team) -> int:
        return obj.titles.all().count()
