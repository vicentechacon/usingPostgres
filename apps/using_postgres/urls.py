from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('nuevo', views.nuevo),
    path('info/<int:idUsuario>', views.info),
    path('editar/<int:idUsuario>', views.editar),
    path('confirmar/eliminar/<int:idUsuario>', views.confirmarEliminacion), 
    path('eliminar/<int:idUsuario>', views.eliminar, name='eliminarUsuario'),
    path('mensajes', views.nuevoMensaje),
    path('like/<int:idMensaje>', views.like),
    path('login', views.login),
    path('cerrarSession', views.cerrarSession),

]
