
from django import forms
from .models import Venta, Producto


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = [
            'punto_venta',
            'medio_pago',
            'modalidad_atencion',
        ]

        widgets = {
            'punto_venta': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'medio_pago': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'modalidad_atencion': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }


class DetalleVentaForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),
        label='Producto'
    )

    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Cantidad'
    )
