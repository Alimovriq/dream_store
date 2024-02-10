from django_filters import rest_framework as filters

from news.models import News, Comments


class NewsFilter(filters.FilterSet):
    """
    Фильтрация для новостей.
    """

    class Meta:
        model = News
        fields = ('title',)


class CommentFilter(filters.FilterSet):
    """
    Фильтрация для новостей.
    """

    class Meta:
        model = Comments
        fields = (
            'author',
            'pub_date',
            'text',
        )
