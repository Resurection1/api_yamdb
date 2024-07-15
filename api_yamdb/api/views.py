from rest_framework import viewsets, mixins, permissions, filters

from django.shortcuts import get_object_or_404


class CommentViewSet(viewsets.ModelViewSet):
    ...


class ReviewViewSet(viewsets.ModelViewSet):
    ...


class CategoryViewSet(viewsets.ModelViewSet):
    ...


class GenreViewSet(viewsets.ModelViewSet):
    ...


class TitleViewSet(viewsets.ModelViewSet):
    ...
