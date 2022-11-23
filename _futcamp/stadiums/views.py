from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from utils import SerializerByMethodMixin, IsAdminOrReadOnly
from .serializers import StadiumSerializer, StadiumDetailSerializer
from .models import Stadium


class StadiumView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Stadium.objects.all()
    serializer_map = {
        "GET": StadiumSerializer,
        "POST": StadiumDetailSerializer,
    }

    def perform_create(self, serializer):
        list_keys = self.request.data.keys()

        if "team_owner" in list_keys:
            team_id = self.request.data["team_owner"]
            return serializer.save(team_owner=team_id)

        return serializer.save()


class StadiumDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = StadiumDetailSerializer
    queryset = Stadium.objects.all()

    lookup_url_kwarg = "stadium_id"

    def perform_update(self, serializer):
        list_keys = self.request.data.keys()

        if "team_owner" in list_keys:
            team_id = self.request.data["team_owner"]
            return serializer.save(team_owner=team_id)

        return serializer.save()
