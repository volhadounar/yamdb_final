from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class WithNoRetreive(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    pass
