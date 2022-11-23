from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Championship
from .serializer import ChampionshipSerializer, ChampionshipDetailSerializer
from utils import IsAdminOrReadOnly, SerializerByMethodMixin


class ChampionshipView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Championship.objects.all()
    serializer_map = {
        "GET": ChampionshipSerializer,
        "POST": ChampionshipDetailSerializer,
    }

    def perform_create(self, serializer):
        list_keys = self.request.data.keys()

        if "teams" in list_keys:
            serializer.save(teams=self.request.data["teams"])

        serializer.save()


class ChampionshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = ChampionshipDetailSerializer
    queryset = Championship.objects.all()

    lookup_url_kwarg = "championship_id"

    def perform_update(self, serializer):
        list_keys = self.request.data.keys()

        if "teams" in list_keys:
            serializer.save(teams=self.request.data["teams"])

        serializer.save()
