from django.contrib import admin
from django.utils.html import format_html

from news.models import News, Comments

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Админка для новостей.
    """

    list_display = (
        'pk',
        'pub_date',
        'title',
        'text',
        'image_preview',
        'slug',
        'meta_title',
        'meta_description',)
    list_filter = (
        'title',
        'pub_date',)

    @admin.display(description='Изображение')
    def image_preview(self, obj):
        try:
            return format_html(
                '<img src="{}" style="max-width:50px; max-height:50px"/>'.format(
                    obj.image.url))
        except ValueError:
            pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """
    Админка для комментариев пользователей.
    """

    list_display = (
        'pk',
        'author',
        'news',
        'text',
        'pub_date',
        'is_published',)
    list_filter = (
        'author',
        'news',
        'pub_date',
        'is_published',)
