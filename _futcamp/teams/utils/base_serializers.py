from rest_framework import serializers

from titles.models import Title
from coachs.models import Coach
from players.models import Player
from stadiums.models import Stadium


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


class PlayerSerializer(serializers.ModelSerializer):
    number_of_goals = serializers.IntegerField(min_value=0)
    number_of_titles = serializers.SerializerMethodField()

    class Meta:
        model = Player

        fields = (
            "id",
            "name",
            "number_of_goals",
            "number_of_titles",
            "position",
            "shirt_number",
        )

    def get_number_of_titles(self, obj: Player) -> int:
        return obj.titles.all().count()


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year_of_conquest",
        )
