from django.contrib import admin
from django.urls import path
from gestion import views  # <--- Importante: Importar tus vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservar/', views.crear_reservacion, name='crear_reservacion'), 
    path('lista/', views.lista_reservaciones, name='lista_reservaciones'), # <--- ESTA NUEVA

]