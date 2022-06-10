from django.views import generic


class HomeView(generic.TemplateView):
    """A class to represent homepage view."""

    template_name = "home.html"
