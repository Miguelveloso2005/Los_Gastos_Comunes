from django.db import models
from django.utils.timezone import now

# Create your models here.

class Expense(models.Model):
    department = models.IntegerField()
    period = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pendiente'), ('paid', 'Pagado')])

    def __str__(self):
        return f"Departamento {self.department} - {self.period} - {self.status}"
  
  
  
from django.db import models

class GastoComun(models.Model):
    departamento = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    periodo = models.CharField(max_length=50)
    pagado = models.BooleanField(default=False)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Gasto de {self.departamento} para {self.periodo}"
    
from django.db import models

class Gasto(models.Model):
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.descripcion} - ${self.monto}"




class Residente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    
    
class GastoComún(models.Model):
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.descripcion

