from django import template
from ventas.models import PRODUCTO_CLASES_DICT

register = template.Library()

@register.filter
def get_clase(val):
	return PRODUCTO_CLASES_DICT.get(val)