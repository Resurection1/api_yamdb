from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models

Author = get_user_model()


class Genres(models.Model):  # жанры произведений
    name = models.CharField(max_length=256, )
    slug = models.SlugField(max_length=50, )


class Categories(models.Model):  # категории
    name = models.CharField(max_length=256, )
    slug = models.SlugField(max_length=50, )


class Titles(models.Model):  # произведения
    name = models.CharField(max_length=256,)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        related_name='genres'
    )
    category = models.OneToOneField(
        Categories,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    def __str__(self):
        return self.name


class Reviews(models.Model):  # отзывы на произведения
    text = models.TextField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1), MaxValueValidator(10)
        ],
        default=1,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True
    )


class Comments(models.Model):  # комментарии к отзывам
    text = models.TextField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True
    )
