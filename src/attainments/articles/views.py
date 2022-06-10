from django.views import generic


class HomeView(generic.TemplateView):
    """A view to render the homepage of the articles package."""

    template_name = "attainments/articles/home.html"
