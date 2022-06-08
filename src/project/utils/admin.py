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
