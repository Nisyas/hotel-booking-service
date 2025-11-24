from django.urls import path

from . import views

urlpatterns = [
    path("create", views.room_create, name="room-create"),
    path("delete/<int:room_id>", views.room_delete, name="room-delete"),
    path("list", views.room_list, name="room-list"),
]
