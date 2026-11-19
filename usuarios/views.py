
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from .models import (
    Producto,
    PuntoVenta,
    Venta,
    DetalleVenta,
    Pedido,
)

from .forms import VentaForm, DetalleVentaForm


def inicio(request):
    return render(request, 'usuarios/inicio.html')


class IniciarSesionView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True


@login_required
def panel(request):
    return render(request, 'usuarios/panel.html')


@login_required
def productos(request):
    lista_productos = Producto.objects.filter(activo=True)

    return render(request, 'usuarios/productos.html', {
        'productos': lista_productos
    })


@login_required
def puntos_venta(request):
    lista_puntos = PuntoVenta.objects.filter(activo=True)

    return render(request, 'usuarios/puntos_venta.html', {
        'puntos': lista_puntos
    })


@login_required
def registrar_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_form = DetalleVentaForm(request.POST)

        if venta_form.is_valid() and detalle_form.is_valid():
            producto = detalle_form.cleaned_data['producto']
            cantidad = detalle_form.cleaned_data['cantidad']

            with transaction.atomic():
                venta = venta_form.save(commit=False)
                venta.total = Decimal('0.00')
                venta.save()

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

                venta.total = producto.precio * cantidad
                venta.save(update_fields=['total'])

                if producto.tipo_producto == 'ELABORACION_PROPIA':
                    Pedido.objects.create(
                        venta=venta,
                        estado='PENDIENTE'
                    )

            return redirect('listar_ventas')

    else:
        venta_form = VentaForm()
        detalle_form = DetalleVentaForm()

    return render(request, 'usuarios/registrar_venta.html', {
        'venta_form': venta_form,
        'detalle_form': detalle_form,
    })


@login_required
def listar_ventas(request):
    ventas = Venta.objects.select_related(
        'punto_venta'
    ).prefetch_related(
        'detalles__producto'
    ).order_by('-fecha_venta')

    return render(request, 'usuarios/listar_ventas.html', {
        'ventas': ventas
    })


@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.select_related(
        'venta',
        'venta__punto_venta'
    ).prefetch_related(
        'venta__detalles__producto'
    ).order_by('-fecha_creacion')

    return render(request, 'usuarios/listar_pedidos.html', {
        'pedidos': pedidos
    })


@login_required
def cambiar_estado_pedido(request, pedido_id):

    if request.method == 'POST':

        pedido = get_object_or_404(Pedido, id=pedido_id)

        if pedido.estado == 'PENDIENTE':
            pedido.estado = 'PREPARADO'

        elif pedido.estado == 'PREPARADO':
            pedido.estado = 'ENTREGADO'

        pedido.save()

    return redirect('listar_pedidos')
