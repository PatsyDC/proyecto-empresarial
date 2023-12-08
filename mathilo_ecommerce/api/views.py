from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets

from django.contrib.auth.models import User
from venta.models import Categoria, Producto, PedidoPersonalizado
from venta.carrito import Carrito

from .serializers import (
    UserSerializer,
    CategoriaSerializer,
    ProductoSerializer,
    CarritoSerializer,
    PedidoPersonalizadoSerializer
)

class IndexView(APIView):
    
    def get(self,request):
        lista_categorias = Categoria.objects.all()
        serializer_categoria = CategoriaSerializer(lista_categorias,many=True)
        return Response(serializer_categoria.data)
    
class CategoriaView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    lookup_url_kwarg  = 'categoria_id'
    serializer_class = CategoriaSerializer

##
    
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    lookup_url_kwarg  = 'producto_id'
    serializer_class = ProductoSerializer
    
class ProductoView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

##

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_url_kwarg  = 'user_id'
    serializer_class = UserSerializer
    
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

##

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class CarritoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carrito.objects.all()
    lookup_url_kwarg  = 'carrito_id'
    serializer_class = CarritoSerializer
    
class CarritoView(generics.ListAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

##

class PedidoPersonalizadoViewSet(viewsets.ModelViewSet):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = PedidoPersonalizadoSerializer

class PedidoPersonalizadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PedidoPersonalizado.objects.all()
    lookup_url_kwarg  = 'pedidopersonalizado_id'
    serializer_class = PedidoPersonalizadoSerializer
    
class PedidoPersonalizadoView(generics.ListAPIView):
    queryset = PedidoPersonalizado.objects.all()
    serializer_class = PedidoPersonalizadoSerializer


