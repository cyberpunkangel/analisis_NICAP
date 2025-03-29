from django.urls import path
from . import views

urlpatterns = [
    path("", views.analisis_nicap, name="analisis_nicap"),
    path("descargar-csv/", views.descargar_csv, name="descargar_csv"),
]