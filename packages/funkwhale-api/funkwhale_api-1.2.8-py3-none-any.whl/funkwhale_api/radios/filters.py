import collections

import persisting_theory
from django.core.exceptions import ValidationError
from django.db.models import Q, functions
from django.urls import reverse_lazy

from funkwhale_api.music import models


class RadioFilterRegistry(persisting_theory.Registry):
    def prepare_data(self, data):
        return data()

    def prepare_name(self, data, name=None):
        return data.code

    @property
    def exposed_filters(self):
        return [f for f in self.values() if f.expose_in_api]


registry = RadioFilterRegistry()


def run(filters, **kwargs):
    candidates = kwargs.pop("candidates", models.Track.objects.all())
    final_query = None
    final_query = registry["group"].get_query(candidates, filters=filters, **kwargs)

    if final_query:
        candidates = candidates.filter(final_query)
    return candidates.order_by("pk").distinct()


def validate(filter_config):
    try:
        f = registry[filter_config["type"]]
    except KeyError:
        raise ValidationError('Invalid type "{}"'.format(filter_config["type"]))
    f.validate(filter_config)
    return True


def test(filter_config, **kwargs):
    """
    Run validation and also gather the candidates for the given config
    """
    data = {"errors": [], "candidates": {"count": None, "sample": None}}
    try:
        validate(filter_config)
    except ValidationError as e:
        data["errors"] = [e.message]
        return data

    candidates = run([filter_config], **kwargs)
    data["candidates"]["count"] = candidates.count()
    data["candidates"]["sample"] = candidates[:10]

    return data


def clean_config(filter_config):
    f = registry[filter_config["type"]]
    return f.clean_config(filter_config)


class RadioFilter(object):
    help_text = None
    label = None
    fields = []
    expose_in_api = True

    def get_query(self, candidates, **kwargs):
        return candidates

    def clean_config(self, filter_config):
        return filter_config

    def validate(self, config):
        operator = config.get("operator", "and")
        try:
            assert operator in ["or", "and"]
        except AssertionError:
            raise ValidationError('Invalid operator "{}"'.format(config["operator"]))


@registry.register
class GroupFilter(RadioFilter):
    code = "group"
    expose_in_api = False

    def get_query(self, candidates, filters, **kwargs):
        if not filters:
            return

        final_query = None
        for filter_config in filters:
            f = registry[filter_config["type"]]
            conf = collections.ChainMap(filter_config, kwargs)
            query = f.get_query(candidates, **conf)
            if filter_config.get("not", False):
                # query = ~query *should* work but it doesn't (see #950)
                # The line below generate a proper subquery
                query = ~Q(pk__in=candidates.filter(query).values_list("pk", flat=True))

            if not final_query:
                final_query = query
            else:
                operator = filter_config.get("operator", "and")
                if operator == "and":
                    final_query &= query
                elif operator == "or":
                    final_query |= query
                else:
                    raise ValueError('Invalid query operator "{}"'.format(operator))
        return final_query

    def validate(self, config):
        super().validate(config)
        for fc in config["filters"]:
            registry[fc["type"]].validate(fc)


@registry.register
class ArtistFilter(RadioFilter):
    code = "artist"
    label = "Artist"
    help_text = "Select tracks for a given artist"
    fields = [
        {
            "name": "ids",
            "type": "list",
            "subtype": "number",
            "autocomplete": reverse_lazy("api:v1:search"),
            "autocomplete_qs": "q={query}",
            "autocomplete_fields": {
                "remoteValues": "artists",
                "name": "name",
                "value": "id",
            },
            "label": "Artist",
            "placeholder": "Select artists",
        }
    ]

    def clean_config(self, filter_config):
        filter_config = super().clean_config(filter_config)
        filter_config["ids"] = sorted(filter_config["ids"])
        names = (
            models.Artist.objects.filter(pk__in=filter_config["ids"])
            .annotate(__size=functions.Length("name"))
            .order_by("__size", "id")
            .values_list("name", flat=True)
        )
        filter_config["names"] = list(names)
        return filter_config

    def get_query(self, candidates, ids, **kwargs):
        return Q(artist__pk__in=ids)

    def validate(self, config):
        super().validate(config)
        try:
            pks = models.Artist.objects.filter(pk__in=config["ids"]).values_list(
                "pk", flat=True
            )
            diff = set(config["ids"]) - set(pks)
            assert len(diff) == 0
        except KeyError:
            raise ValidationError("You must provide an id")
        except AssertionError:
            raise ValidationError('No artist matching ids "{}"'.format(diff))


@registry.register
class TagFilter(RadioFilter):
    code = "tag"
    fields = [
        {
            "name": "names",
            "type": "list",
            "subtype": "string",
            "autocomplete": reverse_lazy("api:v1:search"),
            "autocomplete_fields": {
                "remoteValues": "tags",
                "name": "name",
                "value": "name",
            },
            "autocomplete_qs": "q={query}",
            "label": "Tags",
            "placeholder": "Select tags",
        }
    ]
    help_text = "Select tracks with a given tag"
    label = "Tag"

    def get_query(self, candidates, names, **kwargs):
        return (
            Q(tagged_items__tag__name__in=names)
            | Q(artist__tagged_items__tag__name__in=names)
            | Q(album__tagged_items__tag__name__in=names)
        )

    def clean_config(self, filter_config):
        filter_config = super().clean_config(filter_config)
        filter_config["names"] = sorted(filter_config["names"])
        names = (
            models.tags_models.Tag.objects.filter(name__in=filter_config["names"])
            .annotate(__size=functions.Length("name"))
            .order_by("__size", "pk")
            .values_list("name", flat=True)
        )
        filter_config["names"] = list(names)
        return filter_config

    def validate(self, config):
        super().validate(config)
        try:
            names = models.tags_models.Tag.objects.filter(
                name__in=config["names"]
            ).values_list("name", flat=True)
            diff = set(config["names"]) - set(names)
            assert len(diff) == 0
        except KeyError:
            raise ValidationError("You must provide a name")
        except AssertionError:
            raise ValidationError('No tag matching names "{}"'.format(diff))
