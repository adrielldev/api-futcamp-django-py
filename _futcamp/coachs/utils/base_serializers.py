from rest_framework import serializers

from teams.models import Team
from players.models import Player
from stadiums.models import Stadium
from titles.models import Title


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
            "hometown",
            "number_of_goals",
            "number_of_titles",
            "position",
            "shirt_number",
        )

    def get_number_of_titles(self, obj: Player) -> int:
        return obj.titles.all().count()


class TeamSerializer(serializers.ModelSerializer):
    stadium = StadiumSerializer(read_only=True)
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
            "stadium",
            "players",
        )

    def get_number_of_players(self, obj: Team) -> int:
        return obj.players.all().count()

    def get_number_of_titles(self, obj: Team) -> int:
        return obj.titles.all().count()


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year_of_conquest",
        )
