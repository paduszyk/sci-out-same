from django.urls import include, path

urlpatterns = [
    path("articles/", include("attainments.articles.urls")),
]
