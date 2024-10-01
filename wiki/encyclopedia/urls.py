from django.urls import path

from . import views

urlpatterns = [
    path("wiki/<str:title>", views.entry, name="entry"),
    path("", views.index, name="index")
]
