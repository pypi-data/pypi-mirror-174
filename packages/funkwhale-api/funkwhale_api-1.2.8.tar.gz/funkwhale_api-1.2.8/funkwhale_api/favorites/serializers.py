from rest_framework import serializers

from funkwhale_api.activity import serializers as activity_serializers
from funkwhale_api.federation import serializers as federation_serializers
from funkwhale_api.music.serializers import (
    TrackActivitySerializer,
    TrackSerializer,
)
from funkwhale_api.users.serializers import UserActivitySerializer, UserBasicSerializer

from drf_spectacular.utils import extend_schema_field

from . import models


class TrackFavoriteActivitySerializer(activity_serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    object = TrackActivitySerializer(source="track")
    actor = UserActivitySerializer(source="user")
    published = serializers.DateTimeField(source="creation_date")

    class Meta:
        model = models.TrackFavorite
        fields = ["id", "local_id", "object", "type", "actor", "published"]

    def get_actor(self, obj):
        return UserActivitySerializer(obj.user).data

    def get_type(self, obj):
        return "Like"


class UserTrackFavoriteSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    user = UserBasicSerializer(read_only=True)
    actor = serializers.SerializerMethodField()

    class Meta:
        model = models.TrackFavorite
        fields = ("id", "user", "track", "creation_date", "actor")
        actor = serializers.SerializerMethodField()

    @extend_schema_field(federation_serializers.APIActorSerializer)
    def get_actor(self, obj):
        actor = obj.user.actor
        if actor:
            return federation_serializers.APIActorSerializer(actor).data


class UserTrackFavoriteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrackFavorite
        fields = ("id", "track", "creation_date")


class SimpleFavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    track = serializers.IntegerField()


class AllFavoriteSerializer(serializers.Serializer):
    results = SimpleFavoriteSerializer(many=True, source="*")
    count = serializers.SerializerMethodField()

    def get_count(self, o) -> int:
        return len(o)
