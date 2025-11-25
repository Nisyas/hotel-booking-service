from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.booking_create, name="booking-create"),
    path("delete/<int:booking_id>/", views.booking_delete, name="booking-delete"),
    path("list/", views.booking_list, name="booking-list"),
]
