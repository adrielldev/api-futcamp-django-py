from django.shortcuts import get_object_or_404

from teams.models import Team
from titles.models import Title
from coachs.models import Coach
from players.models import Player
from stadiums.models import Stadium


def validate_team_fields(validated_data, serializer):
    list_keys = validated_data.keys()

    if "coach" and "stadium" in list_keys:
        coach_id = validated_data.pop("coach")
        stadium_id = validated_data.pop("stadium")

        coach = get_object_or_404(Coach, id=coach_id)
        stadium = get_object_or_404(Stadium, id=stadium_id)

        if "players" in list_keys:
            player_list = validated_data.pop("players")

            if "titles" in list_keys:
                title_list = validated_data.pop("titles")
                return serializer.save(
                    coach=coach,
                    stadium=stadium,
                    players=player_list,
                    titles=title_list,
                )
            return serializer.save(coach=coach, stadium=stadium, players=player_list)

        if "titles" in list_keys:
            title_list = validated_data.pop("titles")
            return serializer.save(
                coach=coach,
                stadium=stadium,
                titles=title_list,
            )
        return serializer.save(coach=coach, stadium=stadium)

    if "coach" in list_keys:
        coach_id = validated_data.pop("coach")
        coach = get_object_or_404(Coach, id=coach_id)

        if "players" in list_keys:
            player_list = validated_data.pop("players")

            if "titles" in list_keys:
                title_list = validated_data.pop("titles")
                return serializer.save(
                    coach=coach,
                    player=player_list,
                    titles=title_list,
                )
            return serializer.save(coach=coach, players=player_list)

        if "titles" in list_keys:
            title_list = validated_data.pop("titles")
            return serializer.save(coach=coach, titles=title_list)

        return serializer.save(coach=coach)

    if "stadium" in list_keys:
        stadium_id = validated_data.pop("stadium")
        stadium = get_object_or_404(Stadium, id=stadium_id)

        if "players" in list_keys:
            player_list = validated_data.pop("players")

            if "titles" in list_keys:
                title_list = validated_data.pop("titles")
                return serializer.save(
                    stadium=stadium,
                    player=player_list,
                    titles=title_list,
                )
            return serializer.save(stadium=stadium, players=player_list)

        if "titles" in list_keys:
            title_list = validated_data.pop("titles")
            return serializer.save(stadium=stadium, titles=title_list)

        return serializer.save(stadium=stadium)

    if "players" in list_keys:
        player_list = validated_data.pop("players")

        if "titles" in list_keys:
            title_list = validated_data.pop("titles")
            return serializer.save(players=player_list, titles=title_list)

        return serializer.save(players=player_list)

    if "titles" in list_keys:
        title_list = validated_data.pop("titles")
        return serializer.save(titles=title_list)

    return serializer.save()


def create_team(validated_data):
    players = validated_data.pop("players", False)
    titles = validated_data.pop("titles", False)
    player_list = []
    title_list = []

    if bool(players):
        for player_id in players:
            player = get_object_or_404(Player, id=player_id)
            player_list.append(player)

    if bool(titles):
        for title_id in titles:
            title = get_object_or_404(Title, id=title_id)
            title_list.append(title)

    team = Team.objects.create(**validated_data)
    team.players.set(player_list)
    team.titles.set(title_list)

    return team


def update_team(instance, validated_data):
    players = validated_data.pop("players", False)
    titles = validated_data.pop("titles", False)
    team = Team.objects.filter(id=instance.id).first()

    if bool(players):
        team.players.clear()

        for player_id in players:
            player = get_object_or_404(Player, id=player_id)
            team.players.add(player)

    if bool(titles):
        for title_id in titles:
            title = get_object_or_404(Title, id=title_id)
            team.titles.add(title)

    for key, value in validated_data.items():
        setattr(instance, key, value)

    instance.save()

    return instance
