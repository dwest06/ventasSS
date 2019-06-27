from django import forms
from .models import *

class VentaForm(forms.Form):
    


    """
    class Meta:
        model = Venta
        fields = ('productos', 'total', 'fecha', 'vendido_por')

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        print('En el init del form')
    """