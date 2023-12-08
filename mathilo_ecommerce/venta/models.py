from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Categoria(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'categorias'
    
    def __str__(self):
        return self.nombre


#
class Producto(models.Model):
    nombre = models.CharField(max_length=250)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=250)
    peso = models.DecimalField(max_digits=4, decimal_places=2)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    ancho = models.DecimalField(max_digits=4, decimal_places=2)
    largo = models.DecimalField(max_digits=4, decimal_places=2)
    material = models.CharField(max_length=250)
    color = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='venta/images')
    stock = models.IntegerField(default=0)  # Por ejemplo, el valor predeterminado se establece en 0

    class Meta:
        verbose_name_plural = 'productos'
    
    def __str__(self):
        return self.nombre

class EstadoCarrito(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'estadoDeCarritos'
    
    def __str__(self):
        return str(self.nombre)


class Departamento(models.Model):
    nombre = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'departamentos'
    
    def __str__(self):
        return self.nombre

#
class Provincia(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)
    nombre = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'provincias'
    
    def __str__(self):
        return self.nombre


#
class Distrito(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, default=1)  # Aquí asumiendo que 1 es el valor predeterminado
    nombre = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'distritos'
    
    def __str__(self):
        return self.nombre

#pago

class Pago(models.Model):
    forma = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'pagos'
    
    def __str__(self):
        return self.forma

class PaypalPago(models.Model):
    from .carrito import Carrito
    email = models.CharField(max_length=250, default='')
    contraseña = models.CharField(max_length=250, default='')
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, default=1)
    total_carrito = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = 'Pagos_de_Paypal'
    
    def calcular_total_carrito(self):
        # Calcula el total del carrito vinculado
        if self.id_carrito:
            return self.id_carrito.total
        return 0

    def save(self, *args, **kwargs):
        # Actualiza el campo total_carrito antes de guardar
        self.total_carrito = self.calcular_total_carrito()
        super(PaypalPago, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

#orden

# class Envio(models.Model):
#     provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
#     distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)
#     calle = models.CharField(max_length=250)

class PedidoPersonalizado(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_id_user')
    mensaje = models.CharField(max_length=540)
    número_celular = models.IntegerField()

    class Meta:
        verbose_name_plural = 'pedidos_personalizados'
    
    def __str__(self):
        return str(self.user) 



# -------------------------------

# Detalles_personalizado
# 	categoria
# 	nombre_producto
# 	altura
# 	ancho
# 	largo
# 	material
# 	color
# 	precio
# 	img

# ---------------------------

# envios_de_pa_personalizados
# 	id_usuario
# 	nombre_producto
# 	id_producto
# 	fecha_pedido
# 	fecha_de_entrega
# 	provincia
# 	distrito
# 	calle
# 	cantidad