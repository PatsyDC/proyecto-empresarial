
from django.db import models
from .models import Producto, EstadoCarrito

class Carrito(models.Model):

    ESTADO_CHOICES = [
        ('GUARDADO', 'Guardado'),
        ('EN_PROCESO', 'En proceso de compra'),
    ]
    
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=None, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    creado = models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(EstadoCarrito, on_delete=models.CASCADE, default=1, null=True)

    def save(self, *args, **kwargs):
        # Si no se ha establecido el estado, establecerlo por defecto en 'EN_PROCESO'
        if not self.estado:
            default_estado = EstadoCarrito.objects.get(id=1)
            self.estado = default_estado
        self.total = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} - Usuario: {self.usuario.username}'


