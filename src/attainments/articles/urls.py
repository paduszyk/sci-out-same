from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home"),
]
