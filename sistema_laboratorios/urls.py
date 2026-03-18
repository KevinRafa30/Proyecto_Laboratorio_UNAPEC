from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'), 
    path('reservar/', views.crear_reservacion, name='crear_reservacion'),
    path('lista/', views.lista_reservaciones, name='lista_reservaciones'),
    path('editar/<int:id>/', views.editar_reservacion, name='editar_reservacion'),
    path('eliminar/<int:id>/', views.eliminar_reservacion, name='eliminar_reservacion'),
    path('exportar/', views.exportar_csv, name='exportar_csv'), 

    # --- RUTAS DE MANTENIMIENTO ---
    path('campus/', views.lista_campus, name='lista_campus'),
    path('edificios/', views.lista_edificios, name='lista_edificios'),
    path('tipo-aulas/', views.lista_tipo_aulas, name='lista_tipo_aulas'),
    path('aulas/', views.lista_aulas, name='lista_aulas'),

    # --- RUTAS DE CREAR / EDITAR ---
    path('campus/nuevo/', views.gestionar_campus, name='crear_campus'),
    path('campus/editar/<int:id>/', views.gestionar_campus, name='editar_campus'),
    
    path('edificios/nuevo/', views.gestionar_edificio, name='crear_edificio'),
    path('edificios/editar/<int:id>/', views.gestionar_edificio, name='editar_edificio'),
    
    path('tipo-aulas/nuevo/', views.gestionar_tipo_aula, name='crear_tipo_aula'),
    path('tipo-aulas/editar/<int:id>/', views.gestionar_tipo_aula, name='editar_tipo_aula'),
    
    path('aulas/nuevo/', views.gestionar_aula, name='crear_aula'),
    path('aulas/editar/<int:id>/', views.gestionar_aula, name='editar_aula'),
]