from rest_framework import filters, mixins, viewsets

from .permissions import IsAnonimReadOnly, IsAdminOrSuperUser


class MixinCreateDestroy(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """Вьюсет, позволяющий осуществлять GET, POST и DELETE запросы.
    Поддерживает переменную slug."""

    permission_classes = (IsAnonimReadOnly | IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
