from rest_framework import serializers

from teams.models import Team
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


class TeamSerializer(serializers.ModelSerializer):
    number_of_titles = serializers.SerializerMethodField()

    class Meta:
        model = Team

        fields = (
            "id",
            "name",
            "number_of_titles",
            "coach",
            "stadium",
        )

    def get_number_of_titles(self, obj: Team) -> int:
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
