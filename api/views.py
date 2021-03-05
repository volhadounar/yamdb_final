from api.filters import TitleFilter
from api.mixins_viewset import WithNoRetreive
from api.models import Category, Genre, Review, Title
from api.permissions import (
    IsAdminOrStaff,
    IsAuthorOrModeratorOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleSerializer,
)

from django.contrib.auth import get_user_model
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet


User = get_user_model()


@action(detail=True, methods=['GET', 'POST'])
class TitlesViewSet(ModelViewSet):
    """"Работа с произведениями"""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (
        IsAdminOrStaff,
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TitleReadSerializer
        return TitleSerializer


class GenresViewSet(WithNoRetreive):
    """Работа с жанрами"""
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = (
        IsAdminOrStaff,
    )
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    http_method_names = ['get', 'post', 'delete']


class CategoriesViewSet(WithNoRetreive):
    """Работа с категориями"""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = (
        IsAdminOrStaff,
    )
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    http_method_names = ['get', 'post', 'delete']


@action(detail=True, methods=['GET', 'POST', 'PATCH', 'DELETE'])
class ReviewViewSet(ModelViewSet):
    """Работа с отзывами"""
    permission_classes = (
        IsAuthorOrModeratorOrReadOnly,
    )
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = generics.get_object_or_404(
            Title, pk=self.kwargs['title_id']
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = generics.get_object_or_404(
            Title, pk=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, title=title)


@action(detail=True, methods=['GET', 'POST', 'PATCH', 'DELETE'])
class CommentsViewSet(ModelViewSet):
    """Работа с комментариями"""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrModeratorOrReadOnly,
    )

    def get_queryset(self):
        review = generics.get_object_or_404(
            Review, pk=self.kwargs['review_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = generics.get_object_or_404(
            Review, pk=self.kwargs['review_id']
        )
        serializer.save(
            author=self.request.user,
            review_id=review.pk,
        )
