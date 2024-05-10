from rest_framework.views import APIView, status, Response
from .models import Album
from .serializers import AlbumSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView
from django.core.paginator import Paginator

class AlbumView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        return paginator.get_page(page)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    


