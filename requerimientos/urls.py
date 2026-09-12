from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("nuevo/", views.nuevo, name="nuevo"),
    path("requerimientos/", views.lista_requerimientos, name="lista_requerimientos"),
    path("requerimientos/<int:id>/", views.detalle_requerimiento, name="detalle_requerimiento")   ,
]