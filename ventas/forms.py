from django import forms
from .models import *
from pprint import pprint

class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        self.fields['instagram'].label = 'Instagram o Link'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            pprint(visible.field.__dict__)

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.label == 'Foto':
                visible.field.widget.attrs['class'] = 'form-control-file mb-10'
            else:
                visible.field.widget.attrs['class'] = 'form-control mb-10'
    
class StockForm(forms.ModelForm):

    class Meta:
        model = Stock
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    