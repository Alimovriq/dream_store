from rest_framework import serializers

from news.models import News, Comments


class NewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для новостей.
    """

    class Meta:
        model = News
        fields = (
            'pk',
            'title',
            'text',
            'image',
            'pub_date',
            'views',
            'slug',
            'meta_title',
            'meta_description',
        )


class CommentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев.
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='email'
    )

    class Meta:
        model = Comments
        fields = (
            'pk',
            'author',
            'text',
            'pub_date',
        )
