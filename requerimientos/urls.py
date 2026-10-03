from django.urls import path

from . import views

app_name = "req"
urlpatterns = [
    path("", views.index, name="index"),
    path("nuevo/", views.nuevo, name="nuevo"),
    path("requerimientos/", views.lista_requerimientos, name="lista_requerimientos"),
    path("requerimientos/<int:id>/editar/", views.editar_requerimiento, name="editar_requerimiento"),
    path("requerimientos/<int:id>/eliminar/", views.eliminar_requerimiento, name="eliminar_requerimiento"),
    path("requerimientos/<int:id>/", views.detalle_requerimiento, name="detalle_requerimiento"),
    path('asistente-ia/', views.asistente_ia, name='asistente_ia'),
]