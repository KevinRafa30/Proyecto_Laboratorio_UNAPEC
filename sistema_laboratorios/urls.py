from django.contrib import admin
from django.urls import path
from gestion import views

# 👇 1. Agrega esta línea para importar el sistema de autenticación
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='gestion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
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

    #Ruta del Check in
    path('check-in/<int:id>/', views.check_in_reserva, name='check_in_reserva'),
    path('finalizar/<int:id>/', views.finalizar_reserva, name='finalizar_reserva'),
    path('historial/', views.historial_reservas, name='historial_reservas'),

    path('campus/eliminar/<int:id>/', views.eliminar_campus, name='eliminar_campus'),
    path('edificios/eliminar/<int:id>/', views.eliminar_edificio, name='eliminar_edificio'),
    path('tipo-aulas/eliminar/<int:id>/', views.eliminar_tipo_aula, name='eliminar_tipo_aula'),
    path('aulas/eliminar/<int:id>/', views.eliminar_aula, name='eliminar_aula'),

    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
]