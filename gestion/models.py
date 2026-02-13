from django.db import models

ESTADOS = [
    ('A', 'Activo'),
    ('I', 'Inactivo'),
]

# 1. Campus 
class Campus(models.Model):
    descripcion = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')

    def __str__(self):
        return self.descripcion

# 2. Edificios 
class Edificio(models.Model):
    descripcion = models.CharField(max_length=100)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE) # Relación con Campus
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')

    def __str__(self):
        return f"{self.descripcion} - {self.campus}"

# 3. Tipos de Aulas 
class TipoAula(models.Model):
    descripcion = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')

    def __str__(self):
        return self.descripcion

# 4. Aulas 
class Aula(models.Model):
    descripcion = models.CharField(max_length=100)
    tipo_aula = models.ForeignKey(TipoAula, on_delete=models.CASCADE)
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    capacidad = models.IntegerField()
    cupos_reservados = models.IntegerField(default=0) # [cite: 36]
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')

    def __str__(self):
        return f"{self.descripcion} ({self.edificio})"

# 5. Usuarios (Quienes reservan) 
class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('P', 'Profesor'),
        ('E', 'Estudiante'),
        ('A', 'Administrativo'),
    ]
    nombre = models.CharField(max_length=150)
    cedula = models.CharField(max_length=11, unique=True)
    no_carnet = models.CharField(max_length=20, unique=True)
    tipo_usuario = models.CharField(max_length=1, choices=TIPOS_USUARIO)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')

    def __str__(self):
        return f"{self.nombre} ({self.no_carnet})"

# 6. Empleados (Quienes asisten) [cite: 45-51]
class Empleado(models.Model):
    TANDAS = [
        ('M', 'Matutina'),
        ('V', 'Vespertina'),
        ('N', 'Nocturna'),
    ]
    nombre = models.CharField(max_length=150)
    cedula = models.CharField(max_length=11, unique=True)
    tanda_labor = models.CharField(max_length=1, choices=TANDAS)
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')

    def __str__(self):
        return self.nombre

# 7. Reservación de Horas [cite: 52-60]
class Reservacion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_reservacion = models.DateField()
    cantidad_horas = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')

    def __str__(self):
        return f"Reserva {self.id} - {self.aula} por {self.usuario}"