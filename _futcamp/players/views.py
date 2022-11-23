from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from players.models import Player
from players.serializers import PlayerSerializer, PlayerDetailSerializer
from utils import IsAdminOrReadOnly, SerializerByMethodMixin


class PlayerView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Player.objects.all()
    serializer_map = {
        "GET": PlayerSerializer,
        "POST": PlayerDetailSerializer,
    }

    def perform_create(self, serializer):
        list_keys = self.request.data.keys()

        if "current_team" in list_keys:
            team_id = self.request.data["current_team"]
            return serializer.save(current_team=team_id)

        return serializer.save()


class PlayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Player.objects.all()
    serializer_class = PlayerDetailSerializer

    lookup_url_kwarg = "player_id"

    def perform_update(self, serializer):
        list_keys = self.request.data.keys()

        if "current_team" in list_keys:
            team_id = self.request.data["current_team"]
            return serializer.save(current_team=team_id)

        return serializer.save()
