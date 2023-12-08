from django.shortcuts import render, redirect, get_object_or_404 #HttpResponse
from django.contrib.auth.decorators import login_required #django propio, inicio de sesión 
from django.http import JsonResponse, JsonResponse #JsonResponse es de paypal
from .models import Producto, Categoria, EstadoCarrito, PaypalPago
from .carrito import Carrito
from django.contrib.auth import logout # para salir
from .forms import CustomUserCreationForm # para registrar un usuario
from django.contrib.auth import authenticate
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import PedidoPersonalizadoForm
from django.contrib.auth import login
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings #####
from .forms import UserPrefilForm
import uuid


# Create your views here.

def Index(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos}) #Es un diccionario que trae todos los productos de la bd

def Nosotros(request):
    return render(request, 'nosotros.html')

def Mostrar_muebles(request):
    # Filtrar los productos de la categoría "Muebles"
    productos_muebles = Producto.objects.filter(categoria__nombre='Muebles')

    context = {
        'productos': productos_muebles,
    }

    return render(request, 'muebles.html', context)

def Mostrar_cuadros(request):
    productos_cuadros = Producto.objects.filter(categoria__nombre='Cuadros')

    context = {
        'productos': productos_cuadros,
    }

    return render(request, 'cuadros.html', context)

def Mostrar_accesorios(request):
    productos_accesorios = Producto.objects.filter(categoria__nombre='Accesorios')
    context = {
        'productos': productos_accesorios,
    }
    return render(request, 'accesorios.html', context)

def Mostrar_wallpaper(request):
    productos_wallpaper = Producto.objects.filter(categoria__nombre='Wallpaper')
    context = {
        'productos': productos_wallpaper,
    }
    return render(request, 'papel_tapiz.html', context)

def Mostrar_calcomanias(request):
    productos_calcomanias = Producto.objects.filter(categoria__nombre='Calcomanias')
    context = {
        'productos': productos_calcomanias,
    }
    return render(request, 'calcomanias.html', context)

def DetalleP(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

@login_required
def RedirectToProfile(request):
    return redirect('perfil_usuario')

@login_required
def PerfilUsuario(request):
    if request.user.is_superuser:
        # Si el usuario es un superusuario, redirígelo al panel de administrador
        return redirect('admin:index')
    else:
        # Obtén los carritos del usuario que han sido comprados
        carritos_comprados = Carrito.objects.filter(usuario=request.user, estado__nombre='Comprado')

        # Puedes agregar más lógica aquí según tus necesidades

        return render(request, 'perfil_usuario.html', {'usuario': request.user, 'carritos_comprados': carritos_comprados})

def Exit(request):
    logout(request)
    return redirect('index')

def Register_user(request):
    data = {'form': CustomUserCreationForm()}

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('perfil_usuario')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)


#carrito

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user, producto=producto)
    estado_comprado = EstadoCarrito.objects.get(nombre='En proceso')
    
    if not creado:
        carrito.cantidad += 1
        carrito.save()
    
    return JsonResponse({'message': 'El producto se ha añadido correctamente'}, status=200)

from django.shortcuts import render

@login_required
def ver_carrito(request):
    # Obtén el estado "Comprado" para usarlo en la exclusión
    estado_comprado = EstadoCarrito.objects.get(nombre='Comprado')

    # Obtén los elementos del carrito excluyendo aquellos con estado "Comprado"
    carrito = Carrito.objects.filter(usuario=request.user).exclude(estado=estado_comprado)

    # Agregar un campo calculado en el queryset de carrito que representa el total para cada item en el carrito
    carrito = carrito.annotate(
        precio_total=ExpressionWrapper(F('producto__precio') * F('cantidad'), output_field=DecimalField(max_digits=10, decimal_places=2))
    )

    # Calcular el total general sumando todos los precios totales
    total_carrito = carrito.aggregate(total=Sum('precio_total')).get('total')

    # Verificar el stock antes de procesar el pago
    if request.method == 'POST' and 'procesar_pago' in request.POST:
        for item in carrito:
            if item.cantidad > item.producto.stock:
                mensaje_stock_insuficiente = "Stock insuficiente para el producto '{}'.".format(item.producto.nombre)
                return render(request, 'carrito.html', {'mensaje_stock_insuficiente': mensaje_stock_insuficiente})

        # Si no hay problemas con el stock, puedes proceder con el procesamiento del pago.
        # Aquí puedes agregar la lógica necesaria para procesar el pago.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_carrito,
        'item_name': 'carrito.id', 
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payment-success')),
        'cancel_url': request.build_absolute_uri(reverse('payment-failed')),
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'paypal': paypal_payment,
        'carrito': carrito, 'total_carrito': total_carrito
    }

    return render(request, 'carrito.html', context)



def PaymentSuccessful(request):
    # Obtén el estado "Comprado"
    estado_comprado = EstadoCarrito.objects.get(nombre='Comprado')

    # Obtén el carrito en proceso
    carrito_en_proceso = Carrito.objects.filter(usuario=request.user, estado__nombre='En proceso').first()

    if carrito_en_proceso:
        # Obtén el producto del carrito en proceso
        producto = carrito_en_proceso.producto

        # Resta el stock del producto
        if producto.stock > 0:
            producto.stock -= 1  # Resta uno al stock, ajusta según tus necesidades
            producto.save()

            # Cambia el estado del carrito a "Comprado"
            carrito_en_proceso.estado = estado_comprado
            carrito_en_proceso.save()

    return redirect('index')  # Redirige a donde desees después de una compra exitosa

def paymentFailed(request):

    carrito = Carrito.objects.filter(usuario=request.user)

    return render(request, 'payment-failed.html', {'carrito': carrito})

def actualizar_cantidad(request, item_id):
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        
        try:
            carrito_item = Carrito.objects.get(id=item_id)
            carrito_item.cantidad = int(cantidad)
            carrito_item.save()
            return JsonResponse({'message': 'Cantidad actualizada correctamente'})
        except Carrito.DoesNotExist:
            return JsonResponse({'error': 'No se encontró el artículo en el carrito'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def eliminar_item(request, item_id):
    if request.method == 'POST':

        Carrito.objects.filter(id=item_id).delete()

        return JsonResponse({'message': 'Producto eliminado del carrito'})
    else:
        return JsonResponse({})


@login_required
def proceso_pago_paypal(request):
    # Obtén el carrito actual del usuario
    carrito = Carrito.objects.filter(usuario=request.user)

    # Calcular el total del carrito
    total_carrito = sum(item.total for item in carrito)
    
    # Supongamos que la transacción con PayPal fue exitosa
    # Entonces, actualizamos el estado del carrito y registramos la transacción
    if transaccion_paypal_exitosa:
        # Actualizar el estado del carrito (marcar como "Comprado")
        for item in carrito:
            item.estado = EstadoCarrito.objects.get(nombre='Comprado')
            item.save()

        # Crear un registro de la transacción en tu modelo PaypalPago
        paypal_pago = PaypalPago.objects.create(
            email='correo@ejemplo.com',  # Deberías obtener esto del usuario o de la transacción real con PayPal
            contraseña='contraseña_segura',  # Deberías manejar las contraseñas de forma segura
            id_carrito=carrito.first(),  # Puedes ajustar esto según tu modelo
            total_carrito=total_carrito
        )

        # Redirigir a una página de confirmación o cualquier otra lógica que necesites
        return render(request, 'confirmacion_pago.html', {'paypal_pago': paypal_pago})

    # Si la transacción con PayPal no fue exitosa, podrías redirigir a una página de error
    return render(request, 'error_pago.html')

########

@login_required
def crear_pedido_personalizado(request):
    if request.method == 'POST':
        form = PedidoPersonalizadoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.user = request.user
            pedido.save()
            return redirect('crear_pedido_personalizado')

    else:
        form = PedidoPersonalizadoForm()

    return render(request, 'pedidos_personalizados.html', {'form': form})

def Boleta(request):
    return render(request, 'boleta.html')

@login_required
def edit_perfil(request):
    user = request.user

    if request.method == 'POST':
        form = UserPrefilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario') 
    else:
        form = UserPrefilForm(instance=user)

    return render(request, 'editarPerfil.html', {'form': form})

# def PaymentSuccessful(request):
#     # Obtén el estado "Comprado"
#     estado_comprado = EstadoCarrito.objects.get(nombre='Comprado')

#     # Obtén los elementos del carrito excluyendo aquellos con estado "Comprado"
#     carrito = Carrito.objects.filter(usuario=request.user).exclude(estado=estado_comprado)

#     # Actualiza el estado de los productos en el carrito a "Comprado"
#     for item in carrito:
#         item.estado = estado_comprado
#         item.save()

#     return render(request, 'index.html')