from django.urls import path
from api.views.news_views import NewsList, NewsRetrieve


urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/<str:slug>/', NewsRetrieve.as_view())
]
