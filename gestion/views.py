from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .forms import ReservacionForm, CampusForm, EdificioForm, TipoAulaForm, AulaForm, UsuarioForm, EmpleadoForm
from .models import Reservacion, Aula, Usuario, Campus, Edificio, TipoAula, Usuario, Empleado
from datetime import date
from django.contrib.auth.decorators import login_required

# --- 1. VISTA DEL DASHBOARD ---
@login_required
def dashboard(request):
    total_reservas = Reservacion.objects.count()
    labs_activos = Aula.objects.filter(estado='A').count()
    reservas_hoy = Reservacion.objects.filter(fecha_reservacion=date.today(), estado='A').count()
    
    # Traemos los últimos 5 para la "Actividad Reciente"
    recientes = Reservacion.objects.all().order_by('-id')[:5]

    return render(request, 'gestion/dashboard.html', {
        'total_reservas': total_reservas,
        'labs_activos': labs_activos,
        'reservas_hoy': reservas_hoy,
        'recientes': recientes
    })

# --- 2. VISTA DE CREAR RESERVACIÓN ---
def crear_reservacion(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            # Extraemos datos para validar conflictos
            aula = form.cleaned_data['aula']
            fecha = form.cleaned_data['fecha_reservacion']
            
            # Solo hay conflicto si ya existe una reserva ACTIVA o PENDIENTE en esa aula/fecha
            conflicto = Reservacion.objects.filter(
                aula=aula, 
                fecha_reservacion=fecha, 
                estado__in=['A', 'P']
            ).exists()
            
            if conflicto:
                messages.error(request, f"⚠️ El aula {aula} ya está ocupada o solicitada en esa fecha.")
            else:
                # Al hacer form.save(), Django guarda el 'estado' que seleccionaste en el HTML
                form.save()
                messages.success(request, "✅ Reservación procesada correctamente.")
                return redirect('lista_reservaciones')
    else:
        form = ReservacionForm()
    
    return render(request, 'gestion/crear_reservacion.html', {'form': form})

# --- 3. VISTA DE LISTA Y BÚSQUEDA ---
def lista_reservaciones(request):
    busqueda = request.GET.get("buscar")
    estado_filtro = request.GET.get("estado", "todas") 

    # 1. Si elige 'todas', excluimos Históricas (I) y Canceladas (C)
    if estado_filtro == 'todas':
        reservas = Reservacion.objects.exclude(estado__in=['I', 'C']).order_by('-fecha_reservacion')
        
    # 2. Si elige Activas (A) o Pendientes (P), filtramos normalmente
    elif estado_filtro in ['A', 'P']:
        reservas = Reservacion.objects.filter(estado=estado_filtro).order_by('-fecha_reservacion')
        
    # 3. SEGURIDAD: Si alguien intenta forzar otro estado en la URL, le mostramos 'todas'
    else:
        reservas = Reservacion.objects.exclude(estado__in=['I', 'C']).order_by('-fecha_reservacion')
        estado_filtro = 'todas'

    if busqueda:
        reservas = reservas.filter(
            Q(usuario__nombre__icontains=busqueda) | 
            Q(aula__descripcion__icontains=busqueda)
        )

    return render(request, 'gestion/lista_reservaciones.html', {
        'reservas': reservas, 
        'busqueda': busqueda,
        'estado_filtro': estado_filtro
    })

# 2. NUEVA VISTA: Para ver el baúl de los recuerdos (Historial)
def historial_reservas(request):
    # Traemos las Inactivas (finalizadas) y las Canceladas
    historial = Reservacion.objects.filter(estado__in=['I', 'C']).order_by('-fecha_reservacion')
    return render(request, 'gestion/historial_reservas.html', {'historial': historial})
# --- 4. VISTAS DE EDITAR Y ELIMINAR ---
def eliminar_reservacion(request, id):
    reserva = get_object_or_404(Reservacion, id=id)
    reserva.estado = 'C'  # 'C' de Cancelada
    reserva.save()
    messages.warning(request, f"🚫 La reserva #RES-00{id} ha sido movida al historial como cancelada.")
    return redirect('lista_reservaciones')

def editar_reservacion(request, id):
    reserva = get_object_or_404(Reservacion, id=id)
    if request.method == 'POST':
        form = ReservacionForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Reservación actualizada correctamente.")
            return redirect('lista_reservaciones')
    else:
        form = ReservacionForm(instance=reserva)
    
    return render(request, 'gestion/crear_reservacion.html', {'form': form})

import csv
from django.http import HttpResponse

# --- 5. VISTA DE EXPORTAR A EXCEL ---
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_reservaciones.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Fecha Reserva', 'Aula', 'Usuario Solicitante', 'Horas', 'Atendido Por', 'Estado'])

    reservas = Reservacion.objects.all().values_list(
        'id', 'fecha_reservacion', 'aula__descripcion', 'usuario__nombre', 'cantidad_horas', 'empleado__nombre', 'estado'
    )

    for reserva in reservas:
        writer.writerow(reserva)

    return response

# --- 6. VISTAS DE MANTENIMIENTOS (CAMPUS, EDIFICIOS, TIPOS DE AULA) ---
def lista_campus(request):
    campus_list = Campus.objects.all().order_by('id')
    return render(request, 'gestion/lista_campus.html', {'campus_list': campus_list})

def lista_edificios(request):
    edificios_list = Edificio.objects.all().order_by('id')
    return render(request, 'gestion/lista_edificios.html', {'edificios_list': edificios_list})

def lista_tipo_aulas(request):
    tipos_list = TipoAula.objects.all().order_by('id')
    return render(request, 'gestion/lista_tipo_aulas.html', {'tipos_list': tipos_list})

# --- 7. VISTA DE LISTA DE AULAS ---
def lista_aulas(request):
    aulas_list = Aula.objects.all().order_by('id')
    return render(request, 'gestion/lista_aulas.html', {'aulas_list': aulas_list})

# --- 8. FUNCIONES DE CREAR / EDITAR MANTENIMIENTOS ---
def gestionar_campus(request, id=None):
    instancia = get_object_or_404(Campus, id=id) if id else None
    if request.method == 'POST':
        form = CampusForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Campus guardado correctamente.")
            return redirect('lista_campus')
    else:
        form = CampusForm(instance=instancia)
    return render(request, 'gestion/formulario_generico.html', {'form': form, 'titulo': 'Campus', 'url_volver': 'lista_campus'})

def gestionar_edificio(request, id=None):
    instancia = get_object_or_404(Edificio, id=id) if id else None
    if request.method == 'POST':
        form = EdificioForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Edificio guardado correctamente.")
            return redirect('lista_edificios')
    else:
        form = EdificioForm(instance=instancia)
    return render(request, 'gestion/formulario_generico.html', {'form': form, 'titulo': 'Edificio', 'url_volver': 'lista_edificios'})

def gestionar_tipo_aula(request, id=None):
    instancia = get_object_or_404(TipoAula, id=id) if id else None
    if request.method == 'POST':
        form = TipoAulaForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tipo de Aula guardado correctamente.")
            return redirect('lista_tipo_aulas')
    else:
        form = TipoAulaForm(instance=instancia)
    return render(request, 'gestion/formulario_generico.html', {'form': form, 'titulo': 'Tipo de Aula', 'url_volver': 'lista_tipo_aulas'})

def gestionar_aula(request, id=None):
    instancia = get_object_or_404(Aula, id=id) if id else None
    if request.method == 'POST':
        form = AulaForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Aula/Laboratorio guardado correctamente.")
            return redirect('lista_aulas')
    else:
        form = AulaForm(instance=instancia)
    return render(request, 'gestion/formulario_generico.html', {'form': form, 'titulo': 'Aula / Laboratorio', 'url_volver': 'lista_aulas'})

# Función para iniciar la reserva (Check-in)
def check_in_reserva(request, id):
    reserva = get_object_or_404(Reservacion, id=id)
    reserva.estado = 'A'  # Pasa a Activa
    reserva.save()
    messages.success(request, f"▶️ Sesión iniciada para {reserva.usuario.nombre}.")
    return redirect('lista_reservaciones')

# Función para terminar la reserva (Check-out)
def finalizar_reserva(request, id):
    reserva = get_object_or_404(Reservacion, id=id)
    reserva.estado = 'I'  # 'I' de Inactiva o Finalizada
    reserva.save()
    messages.info(request, f" Sesión finalizada. El aula {reserva.aula.descripcion} ha sido liberada.")
    return redirect('lista_reservaciones')

# --- FUNCIONES PARA ELIMINAR MANTENIMIENTOS ---
def eliminar_campus(request, id):
    campus = get_object_or_404(Campus, id=id)
    campus.delete()
    messages.success(request, "🗑️ Campus eliminado permanentemente.")
    return redirect('lista_campus')

def eliminar_edificio(request, id):
    edificio = get_object_or_404(Edificio, id=id)
    edificio.delete()
    messages.success(request, "🗑️ Edificio eliminado permanentemente.")
    return redirect('lista_edificios')

def eliminar_tipo_aula(request, id):
    tipo = get_object_or_404(TipoAula, id=id)
    tipo.delete()
    messages.success(request, "🗑️ Tipo de aula eliminado permanentemente.")
    return redirect('lista_tipo_aulas')

def eliminar_aula(request, id):
    aula = get_object_or_404(Aula, id=id)
    aula.delete()
    messages.success(request, "🗑️ Aula/Laboratorio eliminado permanentemente.")
    return redirect('lista_aulas')

# --- GESTIÓN DE USUARIOS ---
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('nombre')
    return render(request, 'gestion/lista_usuarios.html', {'usuarios_list': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Usuario registrado correctamente.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'gestion/crear_usuario.html', {'form': form})

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Usuario actualizado.")
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'gestion/crear_usuario.html', {'form': form})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    # BORRADO LÓGICO: No usamos usuario.delete(), solo cambiamos el estado
    usuario.estado = 'I' 
    usuario.save()
    messages.warning(request, f"🚫 El usuario {usuario.nombre} ha sido desactivado.")
    return redirect('lista_usuarios')

# --- GESTIÓN DE EMPLEADOS ---
def lista_empleados(request):
    empleados = Empleado.objects.all().order_by('nombre')
    return render(request, 'gestion/lista_empleados.html', {'empleados_list': empleados})

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Empleado registrado correctamente.")
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'gestion/crear_empleado.html', {'form': form})

def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Datos del empleado actualizados.")
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'gestion/crear_empleado.html', {'form': form})

def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    # BORRADO LÓGICO: Solo cambiamos el estado
    empleado.estado = 'I' 
    empleado.save()
    messages.warning(request, f"🚫 El empleado {empleado.nombre} ha sido desactivado del sistema.")
    return redirect('lista_empleados')