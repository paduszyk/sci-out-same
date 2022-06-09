from django.apps import apps
from django.contrib import admin
from django.contrib.admin import ModelAdmin as BaseModelAdmin
from django.core.exceptions import FieldDoesNotExist
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from . import render_link


def related_objects_links(
    obj,
    *,
    related_model,
    content_field=None,
    max_count=None,
    list_link=True,
):
    """Return a list of admin links to the change forms of the related objects."""
    # Check the relationship

    if not isinstance(related_model, str):
        related_model = related_model._meta.model_name

    related_object_set = getattr(obj, f"{related_model}_set", None)
    if related_object_set is None or not related_object_set.exists():
        return None

    # Get the links to the related objects change forms

    related_objects_links = [
        render_link(
            href=reverse_lazy(
                f"admin:{object._meta.app_label}_{related_model}_change",
                args=(object.id,),
            ),
            content=getattr(object, content_field or "__str__"),
        )
        for object in related_object_set.all()
    ]

    if max_count is None:
        max_count = len(related_objects_links)

    if len(related_objects_links) > max_count:
        related_objects_links = related_objects_links[:max_count] + [
            f"+ {len(related_objects_links) - max_count}{_(' więcej')}"
        ]

    # Get the link to the changelist view listing all the related objects

    if list_link:
        list_url = reverse_lazy(
            f"admin:{obj._meta.app_label}_{related_model}_changelist"
        )
        list_link = (
            render_link(
                href=(f"{list_url}" f"?{obj._meta.model_name}__id__exact={obj.id}"),
                content=_("Zobacz wszystkie"),
            )
            if len(related_objects_links) > 1
            else None
        )
    else:
        list_link = None

    return related_objects_links + (["", list_link] if list_link else [])


class ModelAdmin(BaseModelAdmin):
    """A class to represent customized ModelAdmin options."""

    add_phrase = _("Dodaj")
    change_phrase = _("Zmień")

    model_accusative = None
    model_genitive_plural = _("obiektów")

    def changeform_view(self, request, object_id, form_url, extra_context):
        extra_context = extra_context or {}
        extra_context.update(
            {
                "title": f"{self.change_phrase} {self.model_accusative or _('obiekt')}"
                if self.get_object(request, object_id)
                else f"{self.add_phrase} {self.model_accusative or _('obiekt')}"
            }
        )
        return super().changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            {
                "name": f"{self.add_phrase} {self.model_accusative or _('obiekt')}",
                "title": f"{_('Wybierz')} {self.model_accusative} {_('do zmiany')}",
            }
        )
        return super().changelist_view(request, extra_context)


class RelatedModelFilter:
    """A class to represent admin filter by the selected field of the related model."""

    NULL_PARAMETER_VALUE = "null"
    NULL_LABEL = "-"

    def __init__(self, model, lookup, field, null=False, null_lookup=None, **kwargs):
        self.model = model
        self.lookup = lookup
        self.field = field
        self.null = null
        self.null_lookup = null_lookup
        self.null_lookup_value = True
        self.title = None
        self.parameter_name = None

        self.__dict__.update(kwargs)

    @classmethod
    def as_filter(cls, model, lookup, field, null=False, null_lookup=None, **kwargs):
        """Return the filter without creating an instance of the class."""
        return cls(
            model,
            lookup,
            field,
            null,
            null_lookup,
            **kwargs,
        ).get_filter()

    def get_filter(self):
        """Return the filter class."""

        class Filter(admin.SimpleListFilter):
            """Filter class to be returned."""

            title = self.get_filter_title()
            parameter_name = self.get_filter_parameter_name()

            def lookups(obj, request, model_admin):
                lookups = [
                    (obj.id, getattr(obj, self.field))
                    for obj in self.model.objects.all()
                ]
                if self.null_lookup:
                    lookups += [(self.NULL_PARAMETER_VALUE, self.NULL_LABEL)]
                return lookups

            def queryset(obj, request, queryset):
                value = obj.value()
                if value:
                    if not value == self.NULL_PARAMETER_VALUE:
                        return queryset.filter(**{self.lookup: value}).distinct()
                    return queryset.filter(**{self.null_lookup: self.null_lookup_value})

        return Filter

    @property
    def model(self):
        """Return the object's `_model` attribute."""
        return self._model

    @model.setter
    def model(self, value):
        """Set the objects' `_model` attribute."""
        if isinstance(value, str):
            self._model = apps.get_model(value)
        else:
            self._model = value

    @property
    def field(self):
        """Return the object's `_field` attribute."""
        return self._field

    @field.setter
    def field(self, value):
        """Set the objects' `_field` attribute."""
        if not hasattr(self.model, value):
            raise FieldDoesNotExist(
                f"The requested {self.model._meta.label} model field "
                f"'{value}' does not exist."
            )
        self._field = value

    @property
    def null_lookup(self):
        """Return the object's `_null_lookup` attribute."""
        return self._null_lookup

    @null_lookup.setter
    def null_lookup(self, value):
        """Return the value to be used by the filter as the `null` value."""
        self._null_lookup = value or f"{self.lookup}__isnull"

    def get_filter_title(self):
        """Return the value for filter class `title` attribute."""
        return self.title or self.model._meta.verbose_name

    def get_filter_parameter_name(self):
        """Return the value for filter class `parameter_name` attribute."""
        return self.parameter_name or self.model._meta.model_name
