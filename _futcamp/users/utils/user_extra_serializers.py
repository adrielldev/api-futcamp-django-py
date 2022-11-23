from rest_framework import serializers

from users.models import User
from users.utils import TeamSerializer, PlayerSerializer, ChampionshipSerializer
from django.shortcuts import get_object_or_404
from teams.models import Team
from players.models import Player
from championships.models import Championship


class UserFavoriteDetailSerializer(serializers.ModelSerializer):
    favorite_teams = TeamSerializer(many=True, read_only=True)
    favorite_players = PlayerSerializer(many=True, read_only=True)
    favorite_championships = ChampionshipSerializer(many=True, read_only=True)

    class Meta:
        model = User

        fields = (
            "id",
            "name",
            "email",
            "password",
            "birthdate",
            "genre",
            "is_superuser",
            "is_active",
            "created_at",
            "updated_at",
            "favorite_teams",
            "favorite_players",
            "favorite_championships",
        )
        extra_kwargs = {"password": {"write_only": True}}

        read_only_fields = [
            "created_at",
            "updated_at",
            "is_active",
            "is_superuser",
        ]

    def update(self, instance: User, validated_data: dict) -> User:
        teams = validated_data.pop("favorite_teams", False)
        players = validated_data.pop("favorite_players", False)
        championships = validated_data.pop("favorite_championships", False)

        if bool(teams):
            for team_id in teams:
                team = get_object_or_404(Team, id=team_id)
                instance.favorite_teams.add(team)

        if bool(players):
            for player_id in players:
                player = get_object_or_404(Player, id=player_id)
                instance.favorite_players.add(player)

        if bool(championships):
            for championship_id in championships:
                championship = get_object_or_404(Championship, id=championship_id)
                instance.favorite_championships.add(championship)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class UserFavoriteRemoveSerializer(serializers.ModelSerializer):
    favorite_teams = TeamSerializer(many=True, read_only=True)
    favorite_players = PlayerSerializer(many=True, read_only=True)
    favorite_championships = ChampionshipSerializer(many=True, read_only=True)

    class Meta:
        model = User

        fields = (
            "id",
            "name",
            "email",
            "password",
            "birthdate",
            "genre",
            "is_superuser",
            "is_active",
            "created_at",
            "updated_at",
            "favorite_teams",
            "favorite_players",
            "favorite_championships",
        )
        extra_kwargs = {"password": {"write_only": True}}

        read_only_fields = [
            "created_at",
            "updated_at",
            "is_active",
            "is_superuser",
        ]

    def update(self, instance: User, validated_data: dict) -> User:
        team_id = validated_data.pop("team", False)
        player_id = validated_data.pop("player", False)
        championship_id = validated_data.pop("championship", False)

        if bool(team_id):
            get_object_or_404(Team, id=team_id)
            instance.favorite_teams.remove(team_id)

        if bool(player_id):
            get_object_or_404(Player, id=player_id)
            instance.favorite_players.remove(player_id)

        if bool(championship_id):
            get_object_or_404(Championship, id=championship_id)
            instance.favorite_championships.remove(championship_id)

        instance.save()

        return instance
