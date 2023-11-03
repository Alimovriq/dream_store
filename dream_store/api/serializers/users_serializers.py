from rest_framework import serializers

from users.models import User, UserProfile


class UserProfileSerilizer(serializers.ModelSerializer):
    """
    Сериализует данные для профиля пользователя
    с определенными полями, которые заданы в
    модели профиля пользователя.
    """

    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'about',)


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для пользователя, среди которых
    есть поле userprofile, в котором хранятся данные
    о профиле пользователя.
    """

    userprofile = UserProfileSerilizer(
          read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'userprofile',
            'date_joined',
            )
