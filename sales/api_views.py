from rest_framework import viewsets
from .models import Product, Dealer, Order
from .serializers import ProductSerializer, DealerSerializer, OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .views import confirm_order

class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DealerViewSet(viewsets.ModelViewSet):

    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):

        order = self.get_object()

        if order.status != "draft":
            return Response(
                {"error": "Only draft orders can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            confirm_order(order)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response({"message": "Order confirmed successfully"})
    


    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):

        order = self.get_object()

        if order.status != "draft":
            return Response(
                {"error": "Only draft orders can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            confirm_order(order)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response({"message": "Order confirmed successfully"})