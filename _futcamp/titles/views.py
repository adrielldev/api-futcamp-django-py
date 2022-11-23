from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from utils import IsAdminOrReadOnly, SerializerByMethodMixin
from .serializers import TitleSerializer, TitleDetailSerializer
from .models import Title


class TitleView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Title.objects.all()
    serializer_map = {
        "GET": TitleSerializer,
        "POST": TitleDetailSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(team=self.request.data["team"])


class TitleDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = TitleDetailSerializer
    queryset = Title.objects.all()

    lookup_url_kwarg = "title_id"
