from rest_framework import generics
from ..models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from ..utils.africa_talks import send_sms


class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        self.send_sms_notification(order)

    def send_sms_notification(self, order):
        customer = order.customer
        order_details = {
            "sms_message": f"Order ({order.id}) for {customer.name}, your order for {order.item} has been received.",
            "phone_no": f"{customer.phone}",
        }
        try:
            response = send_sms(order_details)
            print(response)
        except Exception as e:
            print(f"{e}")
