from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, mixins, permissions, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action

from django.core.exceptions import ValidationError, PermissionDenied

from django.db.models import QuerySet

from django.contrib.auth.models import Permission

from django.shortcuts import get_object_or_404

from reviews.models import Comments, Reviews, Categories, Genres, Titles
from users.models import MyUser

from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    CategoryGetField,
    GenreSerializer,
    GenreGetField,
    TitleSerializer,
    TitleGetSerializer,
    UserCreateSerializer,
    UserRecieveTokenSerializer,
    UserSerializer
)

from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModerOnly
)

from .utils import send_confirmation_code


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса User."""

    queryset = MyUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Создает объект класса User и
        отправляет на почту пользователя код подтверждения."""
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = MyUser.objects.get_or_create(**serializer.validated_data)
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
    """Вьюсет для обьектов модели User."""

    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthorOrAdminOrModerOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
        url_name='get_user'
    )
    def get_user_by_username(self, request, username):
        """Обеспечивает получание данных пользователя по его username и
        управление ими."""
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

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        """Позволяет пользователю получить подробную информацию о себе
        и редактировать её."""
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            # serializer.save()
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerOnly,
    )
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer) -> Response:
        review_id: int = self.kwargs['review_id']
        review: Reviews = get_object_or_404(Reviews, pk=review_id)
        if serializer.is_valid():
            serializer.save(author=self.request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self) -> QuerySet:
        review_id: int = self.kwargs['review_id']
        review: Reviews = get_object_or_404(Reviews, pk=review_id)
        comment_list: QuerySet[Comments] = Comments.objects.filter(
            review=review
        )
        return comment_list

    def get_permissions(self) -> Permission:
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        elif self.request.method == 'POST':
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (IsAuthorOrAdminOrModerOnly,)
        return super(CommentViewSet, self).get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer) -> Response:
        title_id: int = self.kwargs['title_id']
        title: Titles = get_object_or_404(Titles, pk=title_id)
        user_reviews: QuerySet[Reviews] = Reviews.objects.filter(
            title=title,
            author=self.request.user
        )
        if user_reviews.exists():
            raise ValidationError
        serializer.save(author=self.request.user, title=title)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self) -> QuerySet:
        title_id: int = self.kwargs['title_id']
        title: Titles = get_object_or_404(Titles, pk=title_id)
        review_list: QuerySet[Reviews] = Reviews.objects.filter(title=title)
        return review_list

    def get_permissions(self) -> Permission:
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        elif self.request.method == 'POST':
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (IsAuthorOrAdminOrModerOnly,)
        return super(TitleViewSet, self).get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('genre__slug', 'category__slug', '=year', '=name',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self) -> Serializer:
        if self.action == 'list':
            return TitleGetSerializer
        return TitleSerializer

    def get_permissions(self) -> Permission:
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (IsAdmin,)
        return super(TitleViewSet, self).get_permissions()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self) -> Serializer:
        if self.action == 'list':
            return CategorySerializer
        return CategoryGetField

    def get_permissions(self) -> Permission:
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (IsAdmin,)
        return super(CategoryViewSet, self).get_permissions()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self) -> Serializer:
        if self.action == 'list':
            return GenreSerializer
        return GenreGetField

    def get_permissions(self) -> Permission:
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (IsAdmin,)
        return super(GenreViewSet, self).get_permissions()
