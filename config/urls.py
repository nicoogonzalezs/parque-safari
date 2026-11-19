
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from usuarios.views import (
    inicio,
    IniciarSesionView,
    panel,
    productos,
    puntos_venta,
    registrar_venta,
    listar_ventas,
    listar_pedidos,
    cambiar_estado_pedido,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', inicio, name='inicio'),

    path(
        'login/',
        IniciarSesionView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='inicio'),
        name='logout'
    ),

    path(
        'panel/',
        panel,
        name='panel'
    ),

    path(
        'productos/',
        productos,
        name='productos'
    ),

    path(
        'puntos-venta/',
        puntos_venta,
        name='puntos_venta'
    ),

    path(
        'ventas/registrar/',
        registrar_venta,
        name='registrar_venta'
    ),

    path(
        'ventas/',
        listar_ventas,
        name='listar_ventas'
    ),

    path(
        'pedidos/',
        listar_pedidos,
        name='listar_pedidos'
    ),

    path(
        'pedidos/<int:pedido_id>/cambiar-estado/',
        cambiar_estado_pedido,
        name='cambiar_estado_pedido'
    ),
]
