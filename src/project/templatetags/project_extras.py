from django import template
from django.templatetags.static import static

register = template.Library()


@register.inclusion_tag("snippets/tag.html", name="tag")
def get_html_tag(name, closing_tag=False, content=None, **attrs):
    """Return HTML code for rendering a tag."""
    return {
        "name": name,
        "closing_tag": closing_tag,
        "content": content,
        "attrs": attrs,
    }


@register.inclusion_tag("snippets/tag.html", name="css_link")
def get_css_link_html_tag(href, **attrs):
    """Return HTML for rendering CSS link."""
    attrs.update(
        {
            "rel": "stylesheet",
            "type": "text/css",
            "href": static(href),
        }
    )
    return get_html_tag("link", closing_tag=False, content=None, **attrs)
