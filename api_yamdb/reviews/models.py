from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

from reviews.constants import (
    MAX_LENGTH_NAME,
    MAX_LENGTH_SLUG,
    MAX_LENGTH_TEXT,
    REVIEW_MAX_VALUE,
    REVIEW_MIN_VALUE
)
from reviews.validators import max_year_validator

Author = get_user_model()


class BaseGenresCategories(models.Model):
    """Базовый класс для жанров и категорий."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Hазвание жанра',
        db_index=True
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LENGTH_TEXT]


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
        return self.text[:MAX_LENGTH_TEXT]


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
        max_length=MAX_LENGTH_NAME,
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
        verbose_name='Жанр',
        through='TitleGenre'
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
        return self.name[:MAX_LENGTH_TEXT]


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)


class Review(BaseReviewComments):
    """Класс отзывов."""

    score = models.PositiveIntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                REVIEW_MIN_VALUE,
                message=f'Значение должно быть больше {REVIEW_MIN_VALUE}'
            ),
            MaxValueValidator(
                REVIEW_MAX_VALUE,
                message=f'Значение должно быть больше {REVIEW_MAX_VALUE}'
            )
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
