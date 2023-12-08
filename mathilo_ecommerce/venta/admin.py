from django.contrib import admin

from .models import Categoria, Producto, Provincia, Distrito, Pago, PedidoPersonalizado, Departamento, EstadoCarrito, PaypalPago

from .carrito import Carrito

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Provincia)
admin.site.register(Distrito)
admin.site.register(Pago)
admin.site.register(PedidoPersonalizado)
admin.site.register(Carrito)
admin.site.register(Departamento)
admin.site.register(EstadoCarrito)
admin.site.register(PaypalPago)
