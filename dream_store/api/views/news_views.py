from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated, SAFE_METHODS,)

from api.serializers.news_serializers import (
    NewsSerializer, CommentsSerializer,)
from api.filters.news_filters import NewsFilter, CommentFilter
from news.models import News, Comments


class NewsList(ListCreateAPIView):
    """
    Создавать новость может только администратор(стаф).
    Просматривать список новостей может любой
    пользователь.
    """

    lookup_field = 'slug'
    serializer_class = NewsSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter,)
    filterset_class = NewsFilter
    search_fields = ('^title',)
    ordering_fields = ('title', 'pub_date',)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        return News.objects.all().order_by('-pub_date')


class NewsRetrieve(RetrieveUpdateDestroyAPIView):
    """
    Получить конкретную новость по {slug}
    может любой пользователь, но обновлять,
    либо удалять только администратор(стаф).
    """

    queryset = News.objects.all()
    lookup_field = 'slug'
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


class CommentList(ListCreateAPIView):
    """
    Создавать запись и получать список
    записей может любой авторизованный
    пользователь.
    """

    serializer_class = CommentsSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter,
    )
    filterset_class = CommentFilter
    search_fields = ('text',)
    ordering_fields = (
        'author',
        'pub_date',
        )

    def get_queryset(self):
        news = get_object_or_404(
            News,
            slug=self.kwargs.get('slug'))
        return news.comments.filter(is_published=True)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny(),]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        news = get_object_or_404(
            News,
            slug=self.kwargs.get('slug')
        )
        serializer.save(
            author=self.request.user,
            news=news)
