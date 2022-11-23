from rest_framework import serializers
from django.shortcuts import get_object_or_404
from datetime import date

from .models import Coach
from teams.models import Team
from .utils import TeamSerializer, TitleSerializer


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
            "current_team",
        )

    def get_number_of_titles(self, obj: Coach) -> int:
        return obj.titles.all().count()


class CoachDetailSerializer(serializers.ModelSerializer):
    number_of_titles = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    current_team = TeamSerializer(read_only=True)
    titles = TitleSerializer(many=True, read_only=True)

    class Meta:
        model = Coach
        fields = (
            "id",
            "name",
            "birthdate",
            "age",
            "biography",
            "number_of_titles",
            "titles",
            "hometown",
            "current_team",
        )

    def get_age(self, obj: Coach) -> int:
        current_date = date.today()
        coach_birthdate = obj.birthdate

        age = (
            current_date.year
            - coach_birthdate.year
            - (
                (current_date.month, current_date.day)
                < (coach_birthdate.month, coach_birthdate.day)
            )
        )

        return age

    def get_number_of_titles(self, obj: Coach) -> int:
        return obj.titles.all().count()

    def create(self, validated_data: dict) -> Coach:
        team_id = validated_data.pop("current_team", False)

        coach = Coach.objects.create(**validated_data)
        if bool(team_id):
            team = get_object_or_404(Team, id=team_id)
            team.coach = coach
            team.save()

        return coach

    def update(self, instance: Coach, validated_data: dict) -> Coach:
        team_id = validated_data.pop("current_team", False)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if bool(team_id):
            team = get_object_or_404(Team, id=team_id)
            instance.current_team = team

        instance.save()

        return instance
