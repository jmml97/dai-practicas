from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  path('grupos/', views.grupo_lista, name='grupo_lista'),
  path('musicos/', views.musico_lista, name='musico_lista'),
  path('albumes/', views.album_lista, name='album_lista'),
  path('grupos/<int:pk>/editar/', views.grupo_editar, name='grupo_editar'),
  path('grupos/<int:pk>/borrar/', views.grupo_borrar, name='grupo_borrar'),
  path('musicos/<int:pk>/editar/', views.musico_editar, name='musico_editar'),
  path('musicos/<int:pk>/borrar/', views.musico_borrar, name='musico_borrar'),
  path('albumes/<int:pk>/editar/', views.album_editar, name='album_editar'),
  path('albumes/<int:pk>/borrar/', views.album_borrar, name='album_borrar'),
  path('grupos/datos/', views.grupo_datos, name='grupo_datos'),
  path('musicos/datos/', views.musico_datos, name='musico_datos'),
  path('albumes/datos/', views.album_datos, name='album_datos'),
  path('grupos/nuevo/', views.grupo_nuevo, name='grupo_nuevo'),
  path('musicos/nuevo/', views.musico_nuevo, name='musico_nuevo'),
  path('albumes/nuevo/', views.album_nuevo, name='album_nuevo'),
  path('estadisticas/', views.estadisticas, name='estadisticas'),
]