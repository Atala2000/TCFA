from django.urls import path
from .views import CustomerListCreate, OrderListCreate, OrderRetrieveUpdateDestroy

urlpatterns = [
    path('customers/', CustomerListCreate.as_view(), name='customer-list-create'),
    # path('customers/<uuid:pk>/', CustomerRetrieveUpdateDestroy.as_view(), name='customer-detail'),
    path('orders/', OrderListCreate.as_view(), name='order-list-create'),
    path('orders/<uuid:pk>/', OrderRetrieveUpdateDestroy.as_view(), name='order-detail'),
]
