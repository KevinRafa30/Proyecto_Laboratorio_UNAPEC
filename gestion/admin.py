from django.contrib import admin
from .models import Campus, Edificio, TipoAula, Aula, Usuario, Empleado, Reservacion

admin.site.register(Campus)
admin.site.register(Edificio)
admin.site.register(TipoAula)
admin.site.register(Aula)
admin.site.register(Usuario)
admin.site.register(Empleado)
admin.site.register(Reservacion)