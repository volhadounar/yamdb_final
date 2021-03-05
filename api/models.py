from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

User = get_user_model()


class Category(models.Model):
    """Модель Категорий"""
    name = models.CharField(
        max_length=255,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанры"""
    name = models.CharField(
        max_length=255,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Произведения"""
    name = models.CharField(
        max_length=255,
        verbose_name='Произведение',
    )
    year = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name='Год выхода',
        db_index=True,
        validators=[year_validator],
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='genre_titles',
        verbose_name='Жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category_titles',
        verbose_name='Категория произведения',
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзывы"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(
        verbose_name='Отзыв',
        null=True,
        blank=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        verbose_name='Комментарий',
        null=False,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
