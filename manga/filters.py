import django_filters
from .models import Manga


class MangaListFilters(django_filters.FilterSet):

    class Meta:
        model = Manga
        fields = ['genre']