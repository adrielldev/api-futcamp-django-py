from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Game
from teams.models import Team
from stadiums.models import Stadium
from championships.models import Championship
from .utils import StadiumSerializer, TeamSerializer, ChampionshipSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            "id",
            "date",
            "result",
            "round",
            "stadium",
            "teams",
            "championship",
        )
        read_only_fields = [
            "stadium",
            "teams",
            "championship",
        ]


class GameDetailSerializer(serializers.ModelSerializer):
    stadium = StadiumSerializer(read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    championship = ChampionshipSerializer(read_only=True)
    match_result = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = (
            "id",
            "date",
            "result",
            "match_result",
            "round",
            "championship",
            "stadium",
            "teams",
        )
        extra_kwargs = {"result": {"write_only": True}}

    def get_match_result(self, obj: Game):
        return f"{obj.teams.all()[0].name} (home) {obj.result} (away) {obj.teams.all()[1].name}"

    def create(self, validated_data):
        championship_id = validated_data.pop("championship")
        stadium_id = validated_data.pop("stadium")
        teams_id = validated_data.pop("teams", False)
        teams = []

        championship = get_object_or_404(Championship, id=championship_id)
        stadium = get_object_or_404(Stadium, id=stadium_id)

        if bool(teams_id):
            for index, team_id in enumerate(teams_id):
                if index < 2:
                    team = get_object_or_404(Team, id=team_id)
                    teams.append(team)

        game = Game.objects.create(
            **validated_data,
            stadium=stadium,
            championship=championship,
        )
        game.teams.set(teams)

        return game
