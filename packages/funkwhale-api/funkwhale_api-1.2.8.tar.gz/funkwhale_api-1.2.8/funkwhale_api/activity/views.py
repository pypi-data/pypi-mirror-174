from rest_framework import viewsets
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from funkwhale_api.common.permissions import ConditionalAuthentication
from funkwhale_api.favorites.models import TrackFavorite

from . import serializers, utils


class ActivityViewSet(viewsets.GenericViewSet):

    serializer_class = serializers.AutoSerializer
    permission_classes = [ConditionalAuthentication]
    queryset = TrackFavorite.objects.none()

    @extend_schema(operation_id="get_activity")
    def list(self, request, *args, **kwargs):
        activity = utils.get_activity(user=request.user)
        serializer = self.serializer_class(activity, many=True)
        return Response({"results": serializer.data}, status=200)
