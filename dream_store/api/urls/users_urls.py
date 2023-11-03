from django.urls import path, include

from api.views.users_views import UserProfileView, EmailActivation

urlpatterns = [
    path('user_activation/<uid>/<token>', EmailActivation.as_view()),
    path('user_profile/update', UserProfileView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
