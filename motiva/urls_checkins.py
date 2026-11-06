from django.urls import path

from . import views_checkins


urlpatterns = [
    path("checkins/new/", views_checkins.checkin_create, name="checkin_create"),
    path("checkins/<int:pk>/", views_checkins.checkin_detail, name="checkin_detail"),
]
