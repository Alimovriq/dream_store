from django.urls import path
from api.views import news_views as news


urlpatterns = [
    path('news/', news.NewsList.as_view())
]
