from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from utils import IsAdmin, IsOwner
from users.utils import TeamSerializer, PlayerSerializer, ChampionshipSerializer
from users.utils.user_extra_serializers import (
    UserFavoriteDetailSerializer,
    UserFavoriteRemoveSerializer,
)

from users.models import User

from teams.models import Team
from players.models import Player
from championships.models import Championship


class GenericUserListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsOwner]

    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return self.queryset.filter(users__id=self.kwargs["user_id"])


class UserFavoriteTeamView(GenericUserListView):
    serializer_class = TeamSerializer
    queryset = Team.objects


class UserFavoritePlayerView(GenericUserListView):
    serializer_class = PlayerSerializer
    queryset = Player.objects


class UserFavoriteChampionshipView(GenericUserListView):
    serializer_class = ChampionshipSerializer
    queryset = Championship.objects


class UserFavoriteDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsOwner]

    serializer_class = UserFavoriteDetailSerializer
    queryset = User.objects.all()

    lookup_url_kwarg = "user_id"

    def perform_update(self, serializer):
        teams = self.request.data.get("favorite_teams", False)
        players = self.request.data.get("favorite_players", False)
        championships = self.request.data.get("favorite_championships", False)

        if teams:
            return serializer.save(favorite_teams=teams)
        if players:
            return serializer.save(favorite_players=players)
        if championships:
            return serializer.save(favorite_championships=championships)

        return serializer.save()


class UserFavoriteRemoveView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsOwner]

    serializer_class = UserFavoriteRemoveSerializer
    queryset = User.objects.all()

    lookup_url_kwarg = "user_id"

    def perform_update(self, serializer):
        team_id = self.request.data.get("team_id", False)
        player_id = self.request.data.get("player_id", False)
        championship_id = self.request.data.get("championship_id", False)

        if team_id:
            return serializer.save(team=team_id)
        if player_id:
            return serializer.save(player=player_id)
        if championship_id:
            return serializer.save(championship=championship_id)

        return serializer.save()
