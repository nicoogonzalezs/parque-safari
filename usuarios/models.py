from django.db import models


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol

class PuntoVenta(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=150)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'punto_venta'
        verbose_name = 'Punto de venta'
        verbose_name_plural = 'Puntos de venta'

    def __str__(self):
        return self.nombre

class Producto(models.Model):

    TIPOS_PRODUCTO = [
        ('ELABORACION_PROPIA', 'Elaboración propia'),
        ('TERMINADO', 'Producto terminado'),
        ('TICKET_ACTIVIDAD', 'Ticket de actividad'),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    tipo_producto = models.CharField(
        max_length=30,
        choices=TIPOS_PRODUCTO
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    MEDIOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('DEBITO', 'Tarjeta de débito'),
        ('CREDITO', 'Tarjeta de crédito'),
    ]

    MODALIDADES = [
        ('VENTA_RAPIDA', 'Venta rápida'),
        ('CON_MESA', 'Atención con mesa'),
    ]

    punto_venta = models.ForeignKey(
        PuntoVenta,
        on_delete=models.PROTECT
    )

    fecha_venta = models.DateTimeField(auto_now_add=True)

    medio_pago = models.CharField(
        max_length=20,
        choices=MEDIOS_PAGO
    )

    modalidad_atencion = models.CharField(
        max_length=20,
        choices=MODALIDADES,
        default='VENTA_RAPIDA'
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Venta #{self.id} - ${self.total}"

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    class Meta:
        verbose_name = 'Detalle de venta'
        verbose_name_plural = 'Detalles de venta'


class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PREPARADO', 'Preparado'),
        ('ENTREGADO', 'Entregado'),
    ]

    venta = models.OneToOneField(
        Venta,
        on_delete=models.CASCADE,
        related_name='pedido'
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PENDIENTE'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_estado_display()}"

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
