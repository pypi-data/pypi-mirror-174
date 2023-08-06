from rest_framework import serializers

from .. import models


class ApplicationSerializer(serializers.ModelSerializer):
    scopes = serializers.CharField(source="scope")

    class Meta:
        model = models.Application
        fields = ["client_id", "name", "scopes", "created", "updated"]

    def to_representation(self, obj):
        repr = super().to_representation(obj)
        if obj.user_id:
            repr["token"] = obj.token
        return repr


class CreateApplicationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=255)
    scopes = serializers.CharField(source="scope", default="read")

    class Meta:
        model = models.Application
        fields = [
            "client_id",
            "name",
            "scopes",
            "client_secret",
            "created",
            "updated",
            "redirect_uris",
        ]
        read_only_fields = ["client_id", "client_secret", "created", "updated"]

    def to_representation(self, obj):
        repr = super().to_representation(obj)
        if obj.user_id:
            repr["token"] = obj.token
        return repr
