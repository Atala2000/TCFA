from rest_framework import serializers
from ..models import Customer, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['code', 'name', 'phone']

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['order_code', 'customer', 'item', 'amount', 'time']
