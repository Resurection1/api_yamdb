from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from rest_framework import serializers

from api.v1.constants import MAX_LENGTH_EMAIL, MAX_LENGTH_NAME, USERNAME_CHECK
from api.v1.utils import send_confirmation_code
from reviews.models import Categories, Comments, Genres, Review, Title
from users.models import MyUser
from users.validators import username_validator


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор для создания объекта класса MyUser."""

    username = serializers.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=[RegexValidator(
            regex=USERNAME_CHECK,
            message='Имя пользователя содержит недопустимый символ'
        ),
            username_validator,
        ]
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
    )

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя 'me'."""

        email = data.get('email')
        username = data.get('username')
        if MyUser.objects.all().filter(email=email, username=username):
            return data

        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено')

        if MyUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует')

        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует')
        return data

    def create(self, validated_data):
        user, created = MyUser.objects.get_or_create(
            username=validated_data['username'],
            defaults={'email': validated_data['email']}
        )
        if not created:
            user.email = validated_data['email']
            user.save(update_fields=['email'])

        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=user.email, confirmation_code=confirmation_code)
        return user


class UserRecieveTokenSerializer(serializers.Serializer):
    """Сериализатор для объекта класса MyUser при получении токена JWT."""

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
    """Сериализатор для модели MyUser."""

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return username

    def validate_role(self, role):
        if role not in ['user', 'moderator', 'admin']:  # Add your roles here
            raise serializers.ValidationError('Invalid role')
        return role

    def update(self, instance, validated_data):
        if 'role' in validated_data and not self.context[
            'request'
        ].user.is_admin:
            validated_data.pop('role')
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Categories
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genres
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET запросах."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'rating', 'description', 'genre', 'category'
        )


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
        model = Title
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
        fields = (
            'id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для можели отзывов."""
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""

        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data
