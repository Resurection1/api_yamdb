from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genres(models.Model):  # жанры произведений
    name = models.CharField(max_length=256, )
    slug = models.SlugField(max_length=50, )


class Categories(models.Model):  # категории
    name = models.CharField(max_length=256, )
    slug = models.SlugField(max_length=50, )


class Titles(models.Model):  # произведения
    name = models.CharField(max_length=256, filter='name')
    year = models.IntegerField(filter='year')
    description = models.TextField()
    genre = models.ForeignKey(Genres, filter='slug', )
    category = models.OneToOneField(Categories, filter='slug', )

    def __str__(self):
        return self.name


class Reviews(models.Model):  # отзывы на произведения
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='titles'
    )


class Comments(models.Model):  # комментарии к отзывам
    title_id = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
