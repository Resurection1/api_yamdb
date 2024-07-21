from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Reviews, Titles
from users.models import MyUser


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    class Meta:
        model = MyUser
        fields = (
            'username', 'email'
        )

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        if MyUser.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if MyUser.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class UserRecieveTokenSerializer(serializers.Serializer):
    """Сериализатор для объекта класса User при получении токена JWT."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = MyUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return username


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категория."""

    class Meta:
        fields = '__all__'
        model = Categories


class CategoryGetField(serializers.SlugRelatedField):
    """Сериалайзер для поля модели категория."""

    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели жанры."""

    class Meta:
        fields = '__all__'
        model = Genres


class GenreGetField(serializers.SlugRelatedField):
    """Сериалайзер для поля модели жанры."""

    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели произведения(только чтение)."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Titles
        fields = [
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        ]


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при небезопасных запросах."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Titles
        fields = (
            'name', 'year', 'description', 'genre', 'category')

    def to_representation(self, title):
        """Определяет какой сериализатор будет использоваться для чтения."""
        serializer = TitleGetSerializer(title)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели комментарий."""
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comments
        exclude = ['review']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Reviews
        fields = (
            'id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Reviews.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data
