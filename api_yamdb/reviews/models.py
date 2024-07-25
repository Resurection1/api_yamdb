from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from .constants import MAX_LENGTH
from .validators import max_year_validator

Author = get_user_model()


class BaseGenresCategories(models.Model):
    """Базовый класс для жанров и категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание жанра',
        db_index=True
    )
    slug = models.SlugField(
        max_length=30,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LENGTH]


class BaseReviewComments(models.Model):
    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:MAX_LENGTH]


class Genres(BaseGenresCategories):
    """Класс жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Categories(BaseGenresCategories):
    """Класс категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',

    )
    year = models.PositiveIntegerField(
        validators=[max_year_validator],
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True
    )

    class Meta:
        verbose_name = 'Название произведения'
        verbose_name_plural = 'Названия произведений'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LENGTH]


class Review(BaseReviewComments):
    """Класс отзывов."""

    score = models.PositiveIntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(1, message='Значение должно быть больше 1'),
            MaxValueValidator(10, message='Значение должно быть больше 10')
        ],
    )

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comments(BaseReviewComments):
    """Класс комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
