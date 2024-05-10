from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album
from rest_framework.generics import ListCreateAPIView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

class SongView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        return paginator.get_page(page)
    
    def perform_create(self, serializer):
        serializer.save(album_id=self.kwargs.get('pk'))