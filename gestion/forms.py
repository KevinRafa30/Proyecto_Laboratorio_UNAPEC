from django import forms
from .models import Reservacion

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['usuario', 'aula', 'fecha_reservacion', 'cantidad_horas', 'empleado', 'comentario']
        widgets = {
            'fecha_reservacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'aula': forms.Select(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_horas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }