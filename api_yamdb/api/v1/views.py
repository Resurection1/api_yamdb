from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly,
    SAFE_METHODS
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.v1.filters import TitleFilter
from api.v1.mixin import MixinCreateDestroy
from api.v1.permissions import (
    IsAdminOrSuperUser,
    IsAuthorOrAdminOrModerOnly
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleGetSerializer,
    UserCreateSerializer,
    UserRecieveTokenSerializer,
    UserSerializer
)
from api.v1.utils import send_confirmation_code
from reviews.models import Categories, Genres, Review, Title
from users.models import MyUser


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса User."""

    queryset = MyUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Отправляет на почту пользователя код подтверждения."""

        req_username = request.data.get('username')
        req_email = request.data.get('email')
        req_user = self.queryset.filter(
            username=req_username, email=req_email
        )
        if req_user.exists():
            return Response(
                self.serializer_class(req_user.first()).data,
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = MyUser.objects.get_or_create(
            username=serializer.validated_data['username'],
            defaults={'email': serializer.validated_data['email']}
        )

        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=user.email,
            confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReceiveTokenViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """Вьюсет для получения пользователем JWT токена."""

    queryset = MyUser.objects.all()
    serializer_class = UserRecieveTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        """Предоставляет пользователю JWT токен по коду подтверждения."""

        serializer = UserRecieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(MyUser, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = MyUser.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @ action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user'
    )
    def get_user_by_username(self, request, username):
        user = get_object_or_404(MyUser, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @ action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerOnly
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        """Возвращает объект текущего отзыва."""

        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id, title_id=title_id)

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""

        return self.get_review().comments.all().order_by('id')

    def perform_create(self, serializer):
        """Создает комментарий для текущего отзыва."""

        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerOnly
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        """Возвращает объект текущего произведения."""

        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""

        return self.get_title().reviews.all().order_by('id')

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения."""

        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly | IsAdminOrSuperUser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться."""

        if self.request.method == SAFE_METHODS:
            return TitleGetSerializer
        return TitleSerializer


class CategoryViewSet(MixinCreateDestroy):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategorySerializer


class GenreViewSet(MixinCreateDestroy):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenreSerializer
