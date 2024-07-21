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
    rating = serializers.IntegerField()

    class Meta:
        model = Titles
        fields = [
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        ]
        read_only_fields = fields


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели произведения."""
    category = CategoryGetField(
        slug_field='slug', queryset=Categories.objects.all()
    )
    genre = GenreGetField(
        slug_field='slug', queryset=Genres.objects.all(), many=True
    )

    class Meta:
        fields = '__all__'
        model = Titles


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели комментарий."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        exclude = ['review']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Reviews
        exclude = ['titles',]

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Reviews.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data
