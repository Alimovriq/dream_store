from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, SAFE_METHODS)

from api.serializers.news_serializers import (
    NewsSerializer, CommentsSerializer,)
from news.models import News, Comments


class NewsList(ListCreateAPIView):
    """
    Создавать,может только администратор(стаф).
    Просматривать новости может любой.
    """

    queryset = News.objects.all()
    lookup_field = 'slug'
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]
    
