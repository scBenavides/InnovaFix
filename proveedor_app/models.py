from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class VistaIngresoInfo(models.Model):
    ingresoId = models.IntegerField(primary_key=True)
    ingresoValor = models.IntegerField()
    ingresoCantidad = models.IntegerField()
    proveedorNombre = models.CharField(max_length=100)  # supplier name
    direccion = models.CharField(max_length=200)
    usuNombre = models.CharField(max_length=25)
    usuApellido = models.CharField(max_length=25)
    usuCorreo = models.EmailField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ingresoinfo'

class VistaCompraVenta(models.Model):
    clienteNombre = models.CharField(max_length=50)
    ventaId = models.IntegerField(primary_key=True)
    productoNombre = models.CharField(max_length=50)
    ventaCantidad = models.IntegerField()  # quantity of the product in the sale
    productoPrecioUnidad = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'compraventa'


class VistaProcesoIngreso(models.Model):
    ingresoId = models.IntegerField(primary_key=True)
    ingresoValor = models.IntegerField()
    proveedorNombre = models.CharField(max_length=100)
    usuNombre = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'procesoingreso'
        
class Rol (models.Model):
    rolId = models.AutoField(primary_key=True)
    rolNombre = models.CharField(max_length=20)
    rolDescripcion = models.CharField(max_length=150)

    class Meta:
        db_table = 'Rol'

    def __str__(self):
        return self.rolNombre

class Cliente(models.Model):
    clienteCedula = models.CharField(max_length=10, primary_key=True)
    clienteNombre = models.CharField(max_length=25, unique=True)
    clienteApellido = models.CharField(max_length=25)
    clienteUsuario = models.CharField(max_length=10)
    clienteContrasena = models.CharField(max_length=10)
    clienteFoto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
    clienteCorreo = models.EmailField(max_length=50)
    clienteTelefono = models.CharField(max_length=10)
    clienteDireccion = models.CharField(max_length=40)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return f"{self.clienteNombre} {self.clienteApellido}"



class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    proveedorNit = models.CharField(max_length=10, primary_key=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)

    class Meta:
        db_table = 'proveedor'

    def __str__(self):
        return self.nombre


class Ingreso(models.Model):
    ingresoId = models.AutoField(primary_key=True)
    ingresoValor = models.IntegerField()
    ingresoCantidad = models.IntegerField()
    proveedorNit = models.ForeignKey('Proveedor', to_field='proveedorNit', on_delete=models.CASCADE, db_column='proveedorNit')
    usuCedula = models.ForeignKey('Usuario', to_field='usuCedula', on_delete=models.CASCADE, db_column='usuCedula')

    class Meta:
        db_table = 'ingreso'

    def __str__(self):
        return f"Ingreso {self.ingresoId} - Proveedor: {self.proveedorNit.nombre} - Valor: {self.ingresoValor:,}"

class Usuario(models.Model):
    usuCedula = models.CharField(max_length=10, primary_key=True)
    usuUsuario = models.CharField(max_length=10)
    usuNombre = models.CharField(max_length=25, unique=True)
    usuApellido = models.CharField(max_length=25)
    rolId = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='rolId', null=True, blank=True)
    usuContrasena = models.CharField(max_length=10)
    usuCorreo = models.EmailField(max_length=35)
    usuTelefono = models.CharField(max_length=10)
    usuDireccion = models.CharField(max_length=30)
    usuFoto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.usuNombre} {self.usuApellido}"


class Producto(models.Model):
    productoId = models.AutoField(primary_key=True) # Now auto-incremental
    productoNombre = models.CharField(max_length=25)
    productoPrecioUnidad = models.DecimalField(max_digits=12, decimal_places=2)
    productoCantidad = models.IntegerField()
    productoDescripcion = models.CharField(max_length=225)
    ingreso = models.ForeignKey(
        Ingreso,
        on_delete=models.CASCADE,
        db_column='ingresoId'  # <- Real database column name
    )
    class Meta:
        db_table = 'producto'

    def __str__(self):
        return f"{self.productoNombre} - ${self.productoPrecioUnidad} - Stock: {self.productoCantidad}"

class Venta(models.Model):
    ventaId = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(
        Cliente,
        to_field="clienteCedula",   # FK points to clienteCedula
        db_column="clienteCedula",  # This column in venta will be named clienteCedula
        on_delete=models.CASCADE
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta {self.ventaId} - {self.fecha}"
        
class ProductoVenta(models.Model):
    productoventaId = models.AutoField(primary_key=True)
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name="productos",
        db_column='ventaId'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='productoId'
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'producto_venta'

    def __str__(self):
        return f"{self.producto.productoNombre} x {self.cantidad}"
    
class Equipo(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    equipoId = models.AutoField(primary_key=True)
    equipoRef = models.CharField(max_length=30)
    equipoNovedad = models.CharField(max_length=300)
    equipoFecha = models.DateField(auto_now_add=True)
    clienteNombre = models.ForeignKey(Cliente, to_field='clienteNombre', on_delete=models.CASCADE, db_column='clienteNombre')
    usuNombre = models.ForeignKey(Usuario, to_field='usuNombre', on_delete=models.CASCADE, db_column='usuNombre')
    equipoEstado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    class Meta:
        db_table = 'equipo'

    def __str__(self):
        return f"Equipo {self.equipoId} - {self.equipoRef} - Estado: {self.equipoEstado}"