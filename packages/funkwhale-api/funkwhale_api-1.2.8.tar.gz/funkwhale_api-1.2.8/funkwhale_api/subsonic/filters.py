from django_filters import rest_framework as filters

from funkwhale_api.music import models as music_models


class AlbumList2FilterSet(filters.FilterSet):
    type = filters.CharFilter(field_name="_", method="filter_type")

    class Meta:
        model = music_models.Album
        fields = []

    def filter_type(self, queryset, name, value):
        ORDERING = {
            "random": "?",
            "newest": "-creation_date",
            "alphabeticalByArtist": "artist__name",
            "alphabeticalByName": "title",
        }
        if value not in ORDERING:
            return queryset

        return queryset.order_by(ORDERING[value])
