from rest_framework import serializers
from .models import Product, Dealer, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):

    stock = serializers.IntegerField(source="inventory.quantity", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class DealerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dealer
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
            "unit_price",
            "line_total"
        ]
        read_only_fields = ["line_total"]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "dealer",
            "status",
            "total_amount",
            "items",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "order_number",
            "total_amount",
            "created_at",
            "updated_at"
        ]

    def create(self, validated_data):

        items_data = validated_data.pop("items")

        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order