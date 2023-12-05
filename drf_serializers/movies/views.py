from rest_framework import viewsets
from .models import Movie, Resource
from .serializers import MovieSerializer, ResourceSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
