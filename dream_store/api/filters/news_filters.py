from django_filters import rest_framework as filters

from news.models import News


class NewsFilter(filters.FilterSet):
    """
    Фильтрация для новостей.
    """

    class Meta:
        model = News
        fields = ('title',)