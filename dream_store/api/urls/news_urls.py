from django.urls import path

from api.views.news_views import (
    NewsList,
    NewsRetrieve,
    CommentList,
    )


urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/<str:slug>/', NewsRetrieve.as_view()),
    path('news/<str:slug>/comments/', CommentList.as_view()),
]
