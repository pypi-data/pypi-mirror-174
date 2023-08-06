from rest_framework import serializers

from funkwhale_api.music.serializers import TrackSerializer
from funkwhale_api.users.serializers import UserBasicSerializer

from . import filters, models
from .radios import registry


class FilterSerializer(serializers.Serializer):
    type = serializers.CharField(source="code")
    label = serializers.CharField()
    help_text = serializers.CharField()
    fields = serializers.ReadOnlyField()


class RadioSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = models.Radio
        fields = (
            "id",
            "is_public",
            "name",
            "creation_date",
            "user",
            "config",
            "description",
        )
        read_only_fields = ("user", "creation_date")

    def save(self, **kwargs):
        kwargs["config"] = [
            filters.registry[f["type"]].clean_config(f)
            for f in self.validated_data["config"]
        ]

        return super().save(**kwargs)


class RadioSessionTrackSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.RadioSessionTrack
        fields = ("session",)


class RadioSessionTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = models.RadioSessionTrack
        fields = ("id", "session", "position", "track")


class RadioSessionSerializer(serializers.ModelSerializer):

    related_object_id = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = models.RadioSession
        fields = (
            "id",
            "radio_type",
            "related_object_id",
            "user",
            "creation_date",
            "custom_radio",
            "config",
        )

    def validate(self, data):
        radio_conf = registry[data["radio_type"]]()
        if radio_conf.related_object_field:
            try:
                data[
                    "related_object_id"
                ] = radio_conf.related_object_field.to_internal_value(
                    data["related_object_id"]
                )
            except KeyError:
                raise serializers.ValidationError("Radio requires a related object")
        radio_conf.validate_session(data, **self.context)
        return data

    def create(self, validated_data):
        validated_data["user"] = self.context.get("user")
        if validated_data.get("related_object_id"):
            radio = registry[validated_data["radio_type"]]()
            validated_data["related_object"] = radio.get_related_object(
                validated_data["related_object_id"]
            )
        return super().create(validated_data)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        radio_conf = registry[repr["radio_type"]]()
        handler = getattr(radio_conf, "get_related_object_id_repr", None)
        if handler and instance.related_object:
            repr["related_object_id"] = handler(instance.related_object)
        return repr
