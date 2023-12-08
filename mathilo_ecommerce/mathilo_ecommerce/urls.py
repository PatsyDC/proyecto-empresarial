"""
URL configuration for mathilo_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from venta import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Utiliza 'django.contrib.auth.views' en lugar de 'django.contrib.auth.urls'
    path('', views.Index, name='index'),
    path('nosotros/', views.Nosotros, name='nosotros'),
    path('api/',include('api.urls')),
    path('producto/<int:producto_id>/', views.DetalleP, name='detalle_producto'),
    path('accounts/profile/', views.PerfilUsuario, name='perfil_usuario'),
    path('exit/', views.Exit, name='exit'),
    path('register/', views.Register_user, name='register'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='carrito'),
    path('actualizar_cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar_item/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('crear_pedido_personalizado/', views.crear_pedido_personalizado, name='crear_pedido_personalizado'),
    path('muebles/', views.Mostrar_muebles, name='muebles'),
    path('cuadros/', views.Mostrar_cuadros, name='cuadros'),
    path('accesorios/', views.Mostrar_accesorios, name='accesorios'),
    path('papel_tapiz/', views.Mostrar_wallpaper, name='papel_tapiz'),
    path('calcomanias/', views.Mostrar_calcomanias, name='calcomanias'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-success/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/', views.paymentFailed, name='payment-failed'),
    path('boleta/', views.Boleta, name='boleta'),
    path('editar/', views.edit_perfil, name='editarPerfil')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


