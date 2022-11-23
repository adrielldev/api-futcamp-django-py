from rest_framework import serializers

from .models import Team
from .utils import StadiumSerializer, CoachSerializer, PlayerSerializer, TitleSerializer
from .services import create_team, update_team


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

    def get_number_of_titles(self, obj: Team) -> int:
        return obj.titles.all().count()


class TeamDetailSerializer(serializers.ModelSerializer):
    coach = CoachSerializer(read_only=True)
    stadium = StadiumSerializer(read_only=True)
    players = PlayerSerializer(many=True, read_only=True)
    titles = TitleSerializer(many=True, read_only=True)
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
            "titles",
            "stadium",
            "coach",
            "players",
        )

    def get_number_of_players(self, obj: Team) -> int:
        return obj.players.all().count()

    def get_number_of_titles(self, obj: Team) -> int:
        return obj.titles.all().count()

    def create(self, validated_data: dict) -> Team:
        return create_team(validated_data)

    def update(self, instance: Team, validated_data: dict) -> Team:
        return update_team(instance, validated_data)
