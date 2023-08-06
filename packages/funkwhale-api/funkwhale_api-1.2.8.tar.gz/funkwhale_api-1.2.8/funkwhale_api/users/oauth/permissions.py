from rest_framework import permissions
from django.core.exceptions import ImproperlyConfigured

from funkwhale_api.common import preferences

from .. import models
from . import scopes


def normalize(*scope_ids):
    """
    Given an iterable containing scopes ids such as {read, write:playlists}
    will return a set containing all the leaf scopes (and no parent scopes)
    """
    final = set()
    for scope_id in scope_ids:
        try:
            scope_obj = scopes.SCOPES_BY_ID[scope_id]
        except KeyError:
            continue

        if scope_obj.children:
            final = final | {s.id for s in scope_obj.children}
        else:
            final.add(scope_obj.id)
    return final


def should_allow(required_scope, request_scopes):
    if not required_scope:
        return True

    if not request_scopes:
        return False

    return required_scope in normalize(*request_scopes)


METHOD_SCOPE_MAPPING = {
    "get": "read",
    "post": "write",
    "patch": "write",
    "put": "write",
    "delete": "write",
}


class ScopePermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method.lower() in ["options", "head"]:
            return True

        scope_config = getattr(view, "required_scope", "noopscope")
        anonymous_policy = getattr(view, "anonymous_policy", False)
        if anonymous_policy not in [True, False, "setting"]:
            raise ImproperlyConfigured(
                "{} is not a valid value for anonymous_policy".format(anonymous_policy)
            )
        if isinstance(scope_config, str):
            scope_config = {
                "read": "read:{}".format(scope_config),
                "write": "write:{}".format(scope_config),
            }
            action = METHOD_SCOPE_MAPPING[request.method.lower()]
            required_scope = scope_config[action]
        else:
            # we have a dict with explicit viewset actions / scopes
            required_scope = scope_config[view.action]

        token = request.auth

        if isinstance(token, models.AccessToken):
            return self.has_permission_token(token, required_scope)
        elif getattr(request, "scopes", None):
            return should_allow(
                required_scope=required_scope, request_scopes=set(request.scopes)
            )
        elif request.user.is_authenticated:
            user_scopes = scopes.get_from_permissions(**request.user.get_permissions())
            return should_allow(
                required_scope=required_scope, request_scopes=user_scopes
            )
        elif hasattr(request, "actor") and request.actor:
            # we use default anonymous scopes
            user_scopes = scopes.FEDERATION_REQUEST_SCOPES
            return should_allow(
                required_scope=required_scope, request_scopes=user_scopes
            )
        else:
            if anonymous_policy is False:
                return False
            if anonymous_policy == "setting" and preferences.get(
                "common__api_authentication_required"
            ):
                return False

            user_scopes = (
                getattr(view, "anonymous_scopes", set()) | scopes.ANONYMOUS_SCOPES
            )
            return should_allow(
                required_scope=required_scope, request_scopes=user_scopes
            )

    def has_permission_token(self, token, required_scope):

        if token.is_expired():
            return False

        if not token.user:
            return False

        user = token.user
        user_scopes = scopes.get_from_permissions(**user.get_permissions())
        token_scopes = set(token.scopes.keys())
        final_scopes = (
            user_scopes
            & normalize(*token_scopes)
            & token.application.normalized_scopes
            & scopes.OAUTH_APP_SCOPES
        )

        return should_allow(required_scope=required_scope, request_scopes=final_scopes)
