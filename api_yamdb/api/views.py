from rest_framework import viewsets, mixins, permissions, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from django.core.exceptions import ValidationError

from django.db.models import QuerySet

from django.shortcuts import get_object_or_404

from reviews.models import Comments, Reviews, Categories, Genres, Titles

from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    GengreSerializer,
    TitleSerializer,
)

from .permissions import IsAuthorOrAdminOrModerOnly, IsAdminOrReadOnly


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
        comment_list: QuerySet[Comments] = Comments.objects.filter(review=review)
        return comment_list


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerOnly,
    )
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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('genre__slug', 'category__slug', '=year', '=name',)
    http_method_names = ('get', 'post', 'patch', 'delete')


class CategoryViewSet(viewsets.ModelViewSet):
    ...


class GenreViewSet(viewsets.ModelViewSet):
    ...
