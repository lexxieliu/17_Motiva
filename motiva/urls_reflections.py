from django.urls import path

from . import views_reflections


urlpatterns = [
    path("checkins/<int:pk>/reflect/", views_reflections.reflection_edit, name="reflection_edit"),
    path("history/", views_reflections.history_list, name="history_list"),
]
