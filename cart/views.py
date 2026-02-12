from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CartItem
from .serializers import CartSerializer
from products.models import Product

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request: Request) -> Response:
        cart_item = CartItem.objects.filter(user=request.user)
        serializer = CartSerializer(cart_item, many=True)
        return Response(serializer.data)
    
    def post(self, request: Request) -> Response:
        user = request.user
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))


        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response('Product mavjud emas', status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            quantity=quantity
        )

        if not created:
            cart_item.quantity +=1
            cart_item.save()

        serializer = CartSerializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetailView(APIView):
    permission_classes  = [IsAuthenticated]


    def get_object(self, pk:int, user):
        try:
            return CartItem.objects.get(pk=pk, user=user)
        except CartItem.DoesNotExist:
            return None


    def get(self, request: Request, pk:int) -> Response:
        cart_item = self.get_object(pk, request.user)

        if not cart_item:
            return Response('Cart item topilmadi', status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart_item)
        return Response(serializer.data)

    def patch(self, request: Request, pk:int) -> Response:
        cart_item = self.get_object(pk, request.user)

        if not cart_item:
            return Response('Cart item topilmadi', status=status.HTTP_404_NOT_FOUND)
        
        quantity = int(request.data.get('quantity', cart_item.quantity))
        if quantity <=0:
            cart_item.delete()
            return Response('cart item removed', status=status.HTTP_200_OK)
        
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartSerializer(cart_item)
        return Response(serializer.data)
    
    def delete(self, request: Request, pk:int) -> Response:
        cart_item = self.get_object(pk, request.user)

        if not cart_item:
            return Response('Cart item topilmadi', status=status.HTTP_404_NOT_FOUND)
        
        cart_item.delete()
        return Response('Cart item removed', status=status.HTTP_200_OK)
