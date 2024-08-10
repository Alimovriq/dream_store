from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class News(models.Model):
    """
    Модель новостей.
    """

    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок')
    text = models.TextField(
        verbose_name='Текст')
    image = models.ImageField(
        verbose_name='Изображение',
        null=True,
        blank=True,
        upload_to='news/')
    views = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров',
    )
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг')
    meta_title = models.CharField(
        max_length=255,
        verbose_name='Мета-название страницы',
        null=True,
        blank=True)
    meta_description = models.CharField(
        max_length=255,
        verbose_name='Мета-описание страницы',
        null=True,
        blank=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return self.title[:30]


class Comments(models.Model):
    """
    Модель комментариев пользователей.
    """

    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments')
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        verbose_name='Новость',
        related_name='comments')
    text = models.TextField(
        max_length=500,
        verbose_name='Комментарий')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания')
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'Пользователь {self.author} оставил комментарий №{self.pk}'
