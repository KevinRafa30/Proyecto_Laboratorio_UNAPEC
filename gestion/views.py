from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservacionForm
from .models import Reservacion

def crear_reservacion(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            # Datos del formulario
            aula = form.cleaned_data['aula']
            fecha = form.cleaned_data['fecha_reservacion']
            
            # VALIDACIÓN: Verificar si ya existe una reserva en esa Aula y Fecha
            # (Esto cumple con el requisito de evitar conflictos)
            conflicto = Reservacion.objects.filter(
                aula=aula,
                fecha_reservacion=fecha,
                estado='A'  # Solo nos importan las activas
            ).exists()
            
            if conflicto:
                messages.error(request, f"⚠️ El aula {aula} ya está ocupada en esa fecha.")
            else:
                reservacion = form.save(commit=False)
                reservacion.estado = 'A' # Aseguramos que se guarde como Activa
                reservacion.save()
                messages.success(request, "✅ Reservación creada con éxito.")
                return redirect('crear_reservacion') # Recarga la página limpia
    else:
        form = ReservacionForm()

    return render(request, 'gestion/crear_reservacion.html', {'form': form})