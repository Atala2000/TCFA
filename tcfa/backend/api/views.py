from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from ..utils.africa_talks import send_sms
from .filters import OrderFilter


class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code']


class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_class = OrderFilter
    search_fields = ['order_code']

    def perform_create(self, serializer):
        """
        Send an SMS notification to the customer after creating an order
        """
        order = serializer.save()
        self.send_sms_notification(order)

    def send_sms_notification(self, order):
        """
        Send an SMS notification to the customer
        """
        customer = order.customer
        order_details = {
            "sms_message": f"Hi {customer.name}, your order ({order.order_code}) for {order.item} has been successfully recieved. Thank you for choosing us!",
            "phone_no": f"{customer.phone}",
        }
        try:
            response = send_sms(order_details)
            print(response)
        except Exception as e:
            print(f"{e}")

class OrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        order = serializer.save()
        self.send_sms_notification(order)

    def send_sms_notification(self, order):
        """
        Send an SMS notification to the customer after updating an order
        """
        customer = order.customer
        order_details = {
            "sms_message": f"Hi {customer.name}, your order ({order.order_code}) for {order.item} has been successfully updated. Thank you for choosing us!",
            "phone_no": f"{customer.phone}",
        }
        try:
            response = send_sms(order_details)
            print(response)
        except Exception as e:
            print(f"{e}")

    def perform_destroy(self, instance):
        """
        Send an SMS notification to the customer after deleting an order
        """
        customer = instance.customer
        order_details = {
            "sms_message": f"Hi {customer.name}, your order ({instance.order_code}) for {instance.item} has been successfully deleted. Thank you for choosing us!",
            "phone_no": f"{customer.phone}",
        }
        try:
            response = send_sms(order_details)
            print(response)
        except Exception as e:
            print(f"{e}")
        instance.delete()
