# Найти применение для миксина или удалить.

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin)


class ListCreateUpdateDestroyMixin(ListModelMixin, CreateModelMixin,
                                   UpdateModelMixin, DestroyModelMixin,
                                   GenericAPIView):
    pass
