from django.template.loader import render_to_string


def render_link(href, content, **extra_attrs):
    """Render anchor link based on the href, content and extra attributes given."""
    attrs = {"href": href}
    attrs.update(extra_attrs)

    return render_to_string(
        template_name="snippets/tag.html",
        context={
            "name": "a",
            "content": content,
            "closing_tag": True,
            "attrs": attrs,
        },
    )
