from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView, Response, status
from .models import Manga, Rating, Bookmarks, Comments, Likes
from .serializers import MangaCreateSerializer, MangaListSerializer, MangaDetailSerializer, LikesCreateSerializer, \
    RatingCreateSerializer, WatchedCreateSerializer, CommentCreateSerializer, BookmarksSerializer
from .filters import MangaListFilters


class MangaCreateView(generics.CreateAPIView):
    queryset = Manga
    serializer_class = MangaCreateSerializer


class BookmarksView(generics.ListAPIView):
    queryset = Manga.objects.all()
    serializer_class = MangaListSerializer
    def get_queryset(self):
        queryset = Manga.objects.filter(bookmarks__user=self.request.user)
        return queryset


class MangaDetailView(APIView):

    def get(self, request, pk):
        manga = Manga.objects.get(pk=pk)
        serializer = MangaDetailSerializer(manga, context={'request': request})
        # Count of watches + 1
        watches_serializer = WatchedCreateSerializer(data={'manga': pk}, context={'request': request})

        if watches_serializer.is_valid(raise_exception=True):
            watches_serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, pk):
        grade = request.data.pop('grade', None)
        comment = request.data.pop('comment', None)
        bookmark = request.data.pop('bookmark', None)

        if grade:
            serializer = RatingCreateSerializer(data={'manga': pk, 'grade': grade}, context={'request': request})

        elif comment:
            serializer = CommentCreateSerializer(data={'manga': pk, 'text': comment}, context={'request': request})

        elif bookmark:
            serializer = BookmarksSerializer(data={'manga': pk}, context={'request': request})

        else:
            serializer = LikesCreateSerializer(data={'manga': pk}, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            if grade:
                all_grades = Rating.objects.filter(manga=pk)
                middle_grade = sum([obj.grade for obj in all_grades]) / len(all_grades)
                manga = Manga.objects.get(pk=pk)
                manga.grades = middle_grade
                manga.save()

            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        comment_id = request.data.pop('comment_id', None)
        bookmark_id = request.data.pop('bookmark_id', None)

        if comment_id:
            comment = Comments.objects.filter(pk=comment_id).first()
            comment.delete()

        elif bookmark_id:
            bookmark = Bookmarks.objects.filter(pk=bookmark_id).first()
            bookmark.delete()

        else:
            like = Likes.objects.filter(manga=pk, user=request.user).first()
            like.delete()

        return Response(status.HTTP_204_NO_CONTENT)


def popular_watches():
    manga = Manga.objects.all()
    popular_manga = manga.annotate(num_related=Count('watches'))
    popular_now = popular_manga.order_by('-num_related')
    return popular_now


def bestsellers_handler():
    popular_now = popular_watches()
    popular_now_id = popular_now.values_list('id', flat=True)
    bestsellers = Manga.objects.filter(pk__in=popular_now_id, grades__gte=7)
    return bestsellers


class IndexListView(APIView):

    def get(self, request):
        manga = Manga.objects.order_by('-updated_date')
        updated_recently = manga[:5]
        popular = popular_watches()
        bestsellers = bestsellers_handler()

        updated_recently_serializer = MangaListSerializer(updated_recently, many=True, context={'request': request})
        popular_serializer = MangaListSerializer(popular, many=True, context={'request': request})
        bestsellers_serializer = MangaListSerializer(bestsellers, many=True, context={'request': request})

        data = {
            'popular': popular_serializer.data,
            'bestsellers': bestsellers_serializer.data,
            'updated_recently': updated_recently_serializer.data
        }

        return Response(data, status.HTTP_200_OK)


class PopularListView(generics.ListAPIView):
    queryset = Manga.objects.all()
    serializer_class = MangaListSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['grades', 'created_date']
    filterset_class = MangaListFilters

    def get_queryset(self):
        queryset = popular_watches()
        return queryset


class BestSellerListView(generics.ListAPIView):
    queryset = Manga.objects.all()
    serializer_class = MangaListSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['grades', 'created_date']
    filterset_class = MangaListFilters

    def get_queryset(self):
        queryset = bestsellers_handler()
        return queryset

class MangaListView(generics.ListAPIView):
    queryset = Manga.objects.all()
    serializer_class = MangaListSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['grades', 'created_date']
    filterset_class = MangaListFilters