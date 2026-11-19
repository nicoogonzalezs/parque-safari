
from decimal import Decimal

from django.contrib import admin
from django.db.models import F, Sum, DecimalField, ExpressionWrapper

from .models import (
    Rol,
    PuntoVenta,
    Producto,
    Venta,
    DetalleVenta,
    Pedido,
)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_rol',
        'descripcion',
    )

    search_fields = ('nombre_rol',)


@admin.register(PuntoVenta)
class PuntoVentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'ubicacion',
        'activo',
    )

    list_filter = ('activo',)
    search_fields = ('nombre', 'ubicacion')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'tipo_producto',
        'precio',
        'activo',
    )

    list_filter = ('tipo_producto', 'activo')
    search_fields = ('nombre',)


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

    fields = (
        'producto',
        'cantidad',
        'precio_unitario',
    )


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'punto_venta',
        'fecha_venta',
        'medio_pago',
        'modalidad_atencion',
        'total',
    )

    list_filter = (
        'medio_pago',
        'modalidad_atencion',
        'punto_venta',
    )

    search_fields = ('id',)

    readonly_fields = ('total',)

    inlines = [DetalleVentaInline]

    def calcular_total(self, venta):
        total = venta.detalles.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('cantidad') * F('precio_unitario'),
                    output_field=DecimalField(
                        max_digits=12,
                        decimal_places=2
                    )
                )
            )
        )['total']

        venta.total = total or Decimal('0.00')
        venta.save(update_fields=['total'])

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        self.calcular_total(form.instance)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'venta',
        'estado',
        'fecha_creacion',
    )

    list_filter = ('estado',)

    list_editable = ('estado',)

    search_fields = ('id', 'venta__id')

    readonly_fields = ('fecha_creacion',)
