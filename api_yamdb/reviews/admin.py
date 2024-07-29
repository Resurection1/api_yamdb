from django.contrib import admin
from django.db.models import Avg

from reviews.models import Categories, Comments, Genres, Review, Title
from api.v1.constants import AVERAGE_SCORE, LIST_PER_PAGE


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки раздела категорий."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):
    """Класс настройки раздела жанров."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс настройки раздела произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
        'count_reviews',
        'get_rating'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name', 'year', 'category')

    def get_genre(self, object):
        """Получает жанр или список жанров произведения."""

        return '\n'.join((genre.name for genre in object.genre.all()))

    def count_reviews(self, object):
        """Вычисляет количество отзывов на произведение."""

        return object.reviews.count()

    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""

        rating = object.reviews.aggregate(average_score=Avg('score'))
        return round(rating.get('average_score'), AVERAGE_SCORE)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывов."""

    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'score', 'pub_date')
    list_per_page = LIST_PER_PAGE
    search_fields = ('author__username',)


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'pub_date')
    list_per_page = LIST_PER_PAGE
    search_fields = ('author__username',)


admin.site.site_title = 'Администрирование YaMDb'
admin.site.site_header = 'Администрирование YaMDb'
