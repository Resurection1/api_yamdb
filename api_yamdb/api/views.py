from rest_framework import viewsets, mixins, permissions, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django.core.exceptions import ValidationError, PermissionDenied

from django.db.models import QuerySet

from django.contrib.auth.models import Permission

from django.shortcuts import get_object_or_404

from reviews.models import Comments, Reviews, Categories, Genres, Titles

from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    CategoryGetField,
    GenreSerializer,
    GenreGetField,
    TitleSerializer,
    TitleGetSerializer
)

from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModerOnly
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
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
