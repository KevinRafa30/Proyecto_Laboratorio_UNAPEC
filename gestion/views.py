from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .forms import ReservacionForm, CampusForm, EdificioForm, TipoAulaForm, AulaForm
from .models import Reservacion, Aula, Usuario, Campus, Edificio, TipoAula

# --- 1. VISTA DEL DASHBOARD ---
def dashboard(request):
    total_reservas = Reservacion.objects.count()
    total_aulas = Aula.objects.count()
    reservas_activas = Reservacion.objects.filter(estado='A').count()
    
    ultimas_reservas = Reservacion.objects.all().order_by('-fecha_reservacion')[:5]

    return render(request, 'gestion/dashboard.html', {
        'total_reservas': total_reservas,
        'total_aulas': total_aulas,
        'reservas_activas': reservas_activas,
        'ultimas_reservas': ultimas_reservas
    })

# --- 2. VISTA DE CREAR RESERVACIÓN ---
def crear_reservacion(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            aula = form.cleaned_data['aula']
            fecha = form.cleaned_data['fecha_reservacion']
            
            conflicto = Reservacion.objects.filter(
                aula=aula, fecha_reservacion=fecha, estado='A'
            ).exists()
            
            if conflicto:
                messages.error(request, f"⚠️ El aula {aula} ya está ocupada en esa fecha.")
            else:
                reservacion = form.save(commit=False)
                reservacion.estado = 'A'
                reservacion.save()
                messages.success(request, "✅ Reservación creada con éxito.")
                return redirect('lista_reservaciones')
    else:
        form = ReservacionForm()

    return render(request, 'gestion/crear_reservacion.html', {'form': form})

# --- 3. VISTA DE LISTA Y BÚSQUEDA ---
def lista_reservaciones(request):
    busqueda = request.GET.get("buscar")
    reservas = Reservacion.objects.all().order_by('-fecha_reservacion')

    if busqueda:
        reservas = reservas.filter(
            Q(usuario__nombre__icontains=busqueda) | 
            Q(aula__descripcion__icontains=busqueda)
        )

    return render(request, 'gestion/lista_reservaciones.html', {
        'reservas': reservas, 
        'busqueda': busqueda
    })

# --- 4. VISTAS DE EDITAR Y ELIMINAR ---
def eliminar_reservacion(request, id):
    reserva = get_object_or_404(Reservacion, id=id)
    reserva.delete()
    messages.success(request, "🗑️ Reservación eliminada correctamente.")
    return redirect('lista_reservaciones')

def editar_reservacion(request, id):
    reserva = get_object_or_404(Reservacion, id=id)
    if request.method == 'POST':
        form = ReservacionForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Reservación actualizada.")
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