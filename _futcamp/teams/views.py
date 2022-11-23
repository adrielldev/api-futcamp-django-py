from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from utils import IsAdminOrReadOnly, SerializerByMethodMixin
from .serializers import TeamSerializer, TeamDetailSerializer
from .services import validate_team_fields

from .models import Team


class TeamView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Team.objects.all()
    serializer_map = {
        "GET": TeamSerializer,
        "POST": TeamDetailSerializer,
    }

    def perform_create(self, serializer):
        validate_team_fields(self.request.data, serializer)


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = TeamDetailSerializer
    queryset = Team.objects.all()

    lookup_url_kwarg = "team_id"

    def perform_update(self, serializer):
        validate_team_fields(self.request.data, serializer)
