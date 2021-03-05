from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Category, Comment, Genre, Review, Title


class GenreSerializer(ModelSerializer):
    """Сериалайзер Жанры"""

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(ModelSerializer):
    """Сериалайзер Категории"""

    class Meta:
        model = Category
        exclude = ('id',)


class TitleSerializer(ModelSerializer):
    """Сериалайзер Произведения"""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(ModelSerializer):
    """Сериалайзер создания и редактирования Произведения"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    """Сериалайзер Отзывы"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            review = Review.objects.filter(
                author=self.context['request'].user,
                title=self.context['view'].kwargs['title_id'])
            if review.exists():
                raise serializers.ValidationError('Already reviewed')
        return data


class CommentSerializer(ModelSerializer):
    """Сериалайзер Комментарии"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('pub_date',)
