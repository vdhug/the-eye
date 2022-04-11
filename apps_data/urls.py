from django.urls import path

from . import views

urlpatterns = [
    path("event", views.register_event, name="register_event"),
]
