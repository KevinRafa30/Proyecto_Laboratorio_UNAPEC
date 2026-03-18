from django import forms
from .models import Reservacion, Campus, Edificio, TipoAula, Aula

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['usuario', 'aula', 'fecha_reservacion', 'cantidad_horas', 'empleado', 'comentario']
        widgets = {
            'fecha_reservacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'aula': forms.Select(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_horas': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 8, 'placeholder': 'Ej: 2'}),
            'comentario': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Motivo o detalles adicionales de la reservación...'}),
        }

# --- FORMULARIOS DE MANTENIMIENTO ---
class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre del campus...'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class EdificioForm(forms.ModelForm):
    class Meta:
        model = Edificio
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre del edificio...'}),
            'campus': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class TipoAulaForm(forms.ModelForm):
    class Meta:
        model = TipoAula
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Laboratorio de Redes...'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Lab-101...'}),
            'tipo_aula': forms.Select(attrs={'class': 'form-select'}),
            'edificio': forms.Select(attrs={'class': 'form-select'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'cupos_reservados': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }