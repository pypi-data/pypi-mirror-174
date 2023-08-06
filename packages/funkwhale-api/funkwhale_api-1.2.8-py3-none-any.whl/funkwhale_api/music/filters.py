from django.db.models import Q

import django_filters
from django_filters import rest_framework as filters

from funkwhale_api.audio import filters as audio_filters
from funkwhale_api.audio import models as audio_models
from funkwhale_api.common import fields
from funkwhale_api.common import filters as common_filters
from funkwhale_api.common import search
from funkwhale_api.moderation import filters as moderation_filters
from funkwhale_api.tags import filters as tags_filters

from . import models
from . import utils


def filter_tags(queryset, name, value):
    non_empty_tags = [v.lower() for v in value if v]
    for tag in non_empty_tags:
        queryset = queryset.filter(tagged_items__tag__name=tag).distinct()
    return queryset


TAG_FILTER = common_filters.MultipleQueryFilter(method=filter_tags)


class RelatedFilterSet(filters.FilterSet):
    related_type = int
    related_field = "pk"
    related = filters.CharFilter(field_name="_", method="filter_related")

    def filter_related(self, queryset, name, value):
        if not value:
            return queryset.none()
        try:
            pk = self.related_type(value)
        except (TypeError, ValueError):
            return queryset.none()

        try:
            obj = queryset.model.objects.get(**{self.related_field: pk})
        except queryset.model.DoesNotExist:
            return queryset.none()

        queryset = queryset.exclude(pk=obj.pk)
        return tags_filters.get_by_similar_tags(queryset, obj.get_tags())


class ChannelFilterSet(filters.FilterSet):

    channel = filters.CharFilter(field_name="_", method="filter_channel")

    def filter_channel(self, queryset, name, value):
        if not value:
            return queryset

        channel = (
            audio_models.Channel.objects.filter(uuid=value)
            .select_related("library")
            .first()
        )

        if not channel:
            return queryset.none()

        uploads = models.Upload.objects.filter(library=channel.library)
        actor = utils.get_actor_from_request(self.request)
        uploads = uploads.playable_by(actor)
        ids = uploads.values_list(self.Meta.channel_filter_field, flat=True)
        return queryset.filter(pk__in=ids).distinct()


class LibraryFilterSet(filters.FilterSet):

    library = filters.CharFilter(field_name="_", method="filter_library")

    def filter_library(self, queryset, name, value):
        if not value:
            return queryset

        actor = utils.get_actor_from_request(self.request)
        library = models.Library.objects.filter(uuid=value).viewable_by(actor).first()

        if not library:
            return queryset.none()

        uploads = models.Upload.objects.filter(library=library)
        uploads = uploads.playable_by(actor)
        ids = uploads.values_list(self.Meta.library_filter_field, flat=True)
        qs = queryset.filter(pk__in=ids).distinct()
        return qs


class ArtistFilter(
    RelatedFilterSet,
    LibraryFilterSet,
    audio_filters.IncludeChannelsFilterSet,
    moderation_filters.HiddenContentFilterSet,
):

    q = fields.SearchFilter(search_fields=["name"], fts_search_fields=["body_text"])
    playable = filters.BooleanFilter(field_name="_", method="filter_playable")
    has_albums = filters.BooleanFilter(field_name="_", method="filter_has_albums")
    tag = TAG_FILTER
    content_category = filters.CharFilter("content_category")
    scope = common_filters.ActorScopeFilter(
        actor_field="tracks__uploads__library__actor",
        distinct=True,
        library_field="tracks__uploads__library",
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("name", "name"),
            ("creation_date", "creation_date"),
            ("modification_date", "modification_date"),
            ("?", "random"),
            ("tag_matches", "related"),
        )
    )

    class Meta:
        model = models.Artist
        fields = {
            "name": ["exact", "iexact", "startswith", "icontains"],
            "mbid": ["exact"],
        }
        hidden_content_fields_mapping = moderation_filters.USER_FILTER_CONFIG["ARTIST"]
        include_channels_field = "channel"
        library_filter_field = "track__artist"

    def filter_playable(self, queryset, name, value):
        actor = utils.get_actor_from_request(self.request)
        return queryset.playable_by(actor, value).distinct()

    def filter_has_albums(self, queryset, name, value):
        if value is True:
            return queryset.filter(albums__isnull=False)
        else:
            return queryset.filter(albums__isnull=True)


class TrackFilter(
    RelatedFilterSet,
    ChannelFilterSet,
    LibraryFilterSet,
    audio_filters.IncludeChannelsFilterSet,
    moderation_filters.HiddenContentFilterSet,
):
    q = fields.SearchFilter(
        search_fields=["title", "album__title", "artist__name"],
        fts_search_fields=["body_text", "artist__body_text", "album__body_text"],
    )
    playable = filters.BooleanFilter(field_name="_", method="filter_playable")
    tag = TAG_FILTER
    id = common_filters.MultipleQueryFilter(coerce=int)
    scope = common_filters.ActorScopeFilter(
        actor_field="uploads__library__actor",
        library_field="uploads__library",
        distinct=True,
    )
    artist = filters.ModelChoiceFilter(
        field_name="_", method="filter_artist", queryset=models.Artist.objects.all()
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("creation_date", "creation_date"),
            ("title", "title"),
            ("album__title", "album__title"),
            ("album__release_date", "album__release_date"),
            ("size", "size"),
            ("position", "position"),
            ("disc_number", "disc_number"),
            ("artist__name", "artist__name"),
            ("artist__modification_date", "artist__modification_date"),
            ("?", "random"),
            ("tag_matches", "related"),
        )
    )

    class Meta:
        model = models.Track
        fields = {
            "title": ["exact", "iexact", "startswith", "icontains"],
            "id": ["exact"],
            "album": ["exact"],
            "license": ["exact"],
            "mbid": ["exact"],
        }
        hidden_content_fields_mapping = moderation_filters.USER_FILTER_CONFIG["TRACK"]
        include_channels_field = "artist__channel"
        channel_filter_field = "track"
        library_filter_field = "track"

    def filter_playable(self, queryset, name, value):
        actor = utils.get_actor_from_request(self.request)
        return queryset.playable_by(actor, value).distinct()

    def filter_artist(self, queryset, name, value):
        return queryset.filter(Q(artist=value) | Q(album__artist=value))


class UploadFilter(audio_filters.IncludeChannelsFilterSet):
    library = filters.CharFilter("library__uuid")
    channel = filters.CharFilter("library__channel__uuid")
    track = filters.UUIDFilter("track__uuid")
    track_artist = filters.UUIDFilter("track__artist__uuid")
    album_artist = filters.UUIDFilter("track__album__artist__uuid")
    library = filters.UUIDFilter("library__uuid")
    playable = filters.BooleanFilter(field_name="_", method="filter_playable")
    scope = common_filters.ActorScopeFilter(
        actor_field="library__actor",
        distinct=True,
        library_field="library",
    )
    import_status = common_filters.MultipleQueryFilter(coerce=str)
    q = fields.SmartSearchFilter(
        config=search.SearchConfig(
            search_fields={
                "track_artist": {"to": "track__artist__name"},
                "album_artist": {"to": "track__album__artist__name"},
                "album": {"to": "track__album__title"},
                "title": {"to": "track__title"},
            },
            filter_fields={
                "artist": {"to": "track__artist__name__iexact"},
                "mimetype": {"to": "mimetype"},
                "album": {"to": "track__album__title__iexact"},
                "title": {"to": "track__title__iexact"},
                "status": {"to": "import_status"},
            },
        )
    )

    class Meta:
        model = models.Upload
        fields = [
            "import_status",
            "mimetype",
            "import_reference",
        ]
        include_channels_field = "track__artist__channel"

    def filter_playable(self, queryset, name, value):
        actor = utils.get_actor_from_request(self.request)
        return queryset.playable_by(actor, value)


class AlbumFilter(
    RelatedFilterSet,
    ChannelFilterSet,
    LibraryFilterSet,
    audio_filters.IncludeChannelsFilterSet,
    moderation_filters.HiddenContentFilterSet,
):
    playable = filters.BooleanFilter(field_name="_", method="filter_playable")
    q = fields.SearchFilter(
        search_fields=["title", "artist__name"],
        fts_search_fields=["body_text", "artist__body_text"],
    )
    content_category = filters.CharFilter("artist__content_category")
    tag = TAG_FILTER
    scope = common_filters.ActorScopeFilter(
        actor_field="tracks__uploads__library__actor",
        distinct=True,
        library_field="tracks__uploads__library",
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("creation_date", "creation_date"),
            ("release_date", "release_date"),
            ("title", "title"),
            ("artist__modification_date", "artist__modification_date"),
            ("?", "random"),
            ("tag_matches", "related"),
        )
    )

    class Meta:
        model = models.Album
        fields = ["artist", "mbid"]
        hidden_content_fields_mapping = moderation_filters.USER_FILTER_CONFIG["ALBUM"]
        include_channels_field = "artist__channel"
        channel_filter_field = "track__album"
        library_filter_field = "track__album"

    def filter_playable(self, queryset, name, value):
        actor = utils.get_actor_from_request(self.request)
        return queryset.playable_by(actor, value)


class LibraryFilter(filters.FilterSet):
    q = fields.SearchFilter(
        search_fields=["name"],
    )
    scope = common_filters.ActorScopeFilter(
        actor_field="actor",
        distinct=True,
        library_field="pk",
    )

    class Meta:
        model = models.Library
        fields = ["privacy_level"]
