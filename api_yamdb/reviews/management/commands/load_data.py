from csv import DictReader
from typing import Any

from django.core.management import BaseCommand

from reviews.models import Categories, Comments, Genres, Review, Title
from users.models import MyUser


models = {
    MyUser: 'users.csv',
    Genres: 'genre.csv',
    Categories: 'category.csv',
    Title: 'titles.csv',
    Comments: 'comments.csv',
    Review: 'review.csv',
}


class Command(BaseCommand):
    """Комманда для заполнения базы данных из csv файлов."""
    help = 'Command to automatically populate the database.'

    def handle(self, *args: Any, **options: Any) -> None:
        path = str('static/data/')
        self.stdout.write(
            self.style.WARNING('Import data from csv files to database.')
        )
        for model, csv_file in models.items():
            with open(path + '/' + csv_file, encoding='utf-8') as file:
                rows = DictReader(file)
                for row in rows:
                    model.objects.get_or_create(**row)
                    if model == (Genres or Categories or MyUser):
                        model.objects.get_or_create(**row)
                    # if model == Title:
                    #     ...
                    # if model == Review:
                    #     ...
                    # if model == Comments:
                    #     ...
            self.stdout.write(
                self.style.SUCCESS(f'{model.__name__} import is done.')
            )
