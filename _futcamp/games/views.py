from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Game
from .serializers import GameSerializer, GameDetailSerializer
from utils import IsAdminOrReadOnly, SerializerByMethodMixin

from django_filters import rest_framework as filters


class GameFilter(filters.FilterSet):
    championship = filters.CharFilter(field_name="championship", lookup_expr="exact")
    date = filters.CharFilter(field_name="date", lookup_expr="exact")
    round = filters.CharFilter(field_name="round", lookup_expr="icontains")
    stadium = filters.CharFilter(field_name="stadium", lookup_expr="exact")

    class Meta:
        model = Game
        fields = ["teams"]


class GameView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Game.objects.all()
    serializer_map = {
        "GET": GameSerializer,
        "POST": GameDetailSerializer,
    }

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GameFilter

    def perform_create(self, serializer):
        stadium = self.request.data["stadium"]
        teams = self.request.data["teams"]
        championship = self.request.data["championship"]

        serializer.save(stadium=stadium, teams=teams, championship=championship)


class GameDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    lookup_url_kwarg = "game_id"
