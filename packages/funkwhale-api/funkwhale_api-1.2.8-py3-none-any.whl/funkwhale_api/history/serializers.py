from rest_framework import serializers

from funkwhale_api.activity import serializers as activity_serializers
from funkwhale_api.federation import serializers as federation_serializers
from funkwhale_api.music.serializers import TrackActivitySerializer, TrackSerializer
from funkwhale_api.users.serializers import UserActivitySerializer, UserBasicSerializer

from drf_spectacular.utils import extend_schema_field

from . import models


class ListeningActivitySerializer(activity_serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    object = TrackActivitySerializer(source="track")
    actor = UserActivitySerializer(source="user")
    published = serializers.DateTimeField(source="creation_date")

    class Meta:
        model = models.Listening
        fields = ["id", "local_id", "object", "type", "actor", "published"]

    def get_actor(self, obj):
        return UserActivitySerializer(obj.user).data

    def get_type(self, obj):
        return "Listen"


class ListeningSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    user = UserBasicSerializer(read_only=True)
    actor = serializers.SerializerMethodField()

    class Meta:
        model = models.Listening
        fields = ("id", "user", "track", "creation_date", "actor")

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]

        return super().create(validated_data)

    @extend_schema_field(federation_serializers.APIActorSerializer)
    def get_actor(self, obj):
        actor = obj.user.actor
        if actor:
            return federation_serializers.APIActorSerializer(actor).data


class ListeningWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Listening
        fields = ("id", "user", "track", "creation_date")

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]

        return super().create(validated_data)
