from django.contrib import admin


def related_model_count(related_model, field=None):
    """
    Get a callable returning the count of object of a related model.

    The field storing the counts should be either explicitly defined in models module
    or created by using QuerySet annotations using django.db.models.Count class.
    """
    if field is None:
        field = f"{related_model._meta.model_name}_count"

    @admin.display(
        description=related_model._meta.verbose_name_plural.capitalize(),
        ordering=field,
    )
    def count(obj):
        """Return the count of the related model objects."""
        return getattr(obj, field, None)

    return count
