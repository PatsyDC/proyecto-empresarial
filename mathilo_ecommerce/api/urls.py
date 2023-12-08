from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'producto',views.ProductoViewSet,basename='mathilo')

urlpatterns = [
    path('',views.IndexView.as_view()),
    path('categoria',views.CategoriaView.as_view()),
    path('producto',views.ProductoView.as_view()),
    path('user',views.UserView.as_view()),
    path('carrito',views.CarritoView.as_view()),
    path('pedidoPersonalizado',views.PedidoPersonalizadoView.as_view()),
    path('categoria/<int:categoria_id>',views.CategoriaDetailView.as_view()),
    path('producto/<int:producto_id>',views.ProductoDetailView.as_view()),
    path('user/<int:user_id>',views.UserDetailView.as_view()),
    path('carrito/<int:carrito_id>',views.CarritoDetailView.as_view()),
    path('pedidoPersonalizado/<int:pedidopersonalizado_id>',views.PedidoPersonalizadoDetailView.as_view()),
    path('admin/',include(router.urls))
]