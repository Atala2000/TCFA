from django.urls import path
from .views import CustomerListCreate, OrderListCreate

urlpatterns = [
    path('customers/', CustomerListCreate.as_view(), name='customer-list-create'),
    path('orders/', OrderListCreate.as_view(), name='order-list-create'),
]
