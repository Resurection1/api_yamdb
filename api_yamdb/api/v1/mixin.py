from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .permissions import IsAdminOrSuperUser


class MixinCreateDestroy(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """Вьюсет, позволяющий осуществлять GET, POST и DELETE запросы.
    Поддерживает переменную slug."""

    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly | IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
