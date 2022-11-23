from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from utils import SerializerByMethodMixin, IsAdminOrReadOnly
from .serializers import CoachSerializer, CoachDetailSerializer
from .models import Coach


class CreateListCoachView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Coach.objects.all()
    serializer_map = {
        "GET": CoachSerializer,
        "POST": CoachDetailSerializer,
    }

    def perform_create(self, serializer):
        list_keys = self.request.data.keys()

        if "current_team" in list_keys:
            team_id = self.request.data["current_team"]
            return serializer.save(current_team=team_id)

        return serializer.save()


class GetUpdateDeleteCoachView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = CoachDetailSerializer
    queryset = Coach.objects.all()

    lookup_url_kwarg = "coach_id"

    def perform_update(self, serializer):
        list_keys = self.request.data.keys()

        if "current_team" in list_keys:
            team_id = self.request.data["current_team"]
            return serializer.save(current_team=team_id)

        return serializer.save()
