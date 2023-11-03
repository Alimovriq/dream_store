import json
import requests

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from api.serializers.users_serializers import UserProfileSerilizer


class UserProfileView(APIView):
    """
    Представление для возможности
    редактирования профиля пользователя
    при запросе PUT.
    """

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.request.user.userprofile
        serializer = UserProfileSerilizer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailActivation(APIView):
    """
    Активация пользователя по email.
    """

    def get(self, request, uid, token, format=None):
        """
        При GET запросе передается uid с фронта,
        сгенерированный токен и служебная информация,
        что это json, далее библотека request обрабатывает
        поступившую информацию и передает ее с помощью
        метода post чтобы активировать пользователя.
        """

        payload = {'uid': uid, 'token': token}
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        domain = request.get_host()
        # такой эндпоинт, т.к. это от Djoser
        url = f'http://{domain}/api/v1/auth/users/activation/'
        response = requests.post(url, data=json.dumps(payload),
                                 headers=headers)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({'detail': 'Активация прошла успешно!'},
                            response.status_code)
        return Response(response.json(), response.status_code)
