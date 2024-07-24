from django.test import TestCase, Client
from .models import Customer, Order
import jwt
from datetime import datetime, timedelta
from django.conf import settings

class CustomerTestCase(TestCase):
    def setUp(self):
        Customer.objects.create(name="John Doe", phone="+254712345678")
        Customer.objects.create(name="Jane Doe", phone="+255712345678")

    def test_customer_name(self):
        customer1 = Customer.objects.get(name="John Doe")
        customer2 = Customer.objects.get(name="Jane Doe")
        self.assertEqual(customer1.name, 'John Doe')
        self.assertEqual(customer2.name, 'Jane Doe')

    def test_customer_count(self):
        customer_count = Customer.objects.count()
        self.assertEqual(customer_count, 2)

    def test_customer_creation(self):
        customer = Customer.objects.create(name="Alice Smith", phone="+123456789")
        self.assertEqual(customer.name, "Alice Smith")
        self.assertEqual(customer.phone, "+123456789")

    def test_customer_deletion(self):
        customer = Customer.objects.get(name="John Doe")
        customer.delete()
        self.assertFalse(Customer.objects.filter(name="John Doe").exists())

class OrderTestCase(TestCase):
    def setUp(self):
        customer = Customer.objects.create(name="John Doe", phone="+254712345678")
        Order.objects.create(customer=customer, amount=1000, item="Book")
        Order.objects.create(customer=customer, amount=2000, item="Laptop")

    def test_order_total(self):
        order1 = Order.objects.get(amount=1000)
        order2 = Order.objects.get(amount=2000)
        self.assertEqual(order1.amount, 1000)
        self.assertEqual(order2.amount, 2000)

    def test_order_count(self):
        order_count = Order.objects.count()
        self.assertEqual(order_count, 2)

    def test_order_creation(self):
        customer = Customer.objects.create(name="Alice Smith", phone="+123456789")
        order = Order.objects.create(customer=customer, amount=3000, item="Phone")
        self.assertEqual(order.amount, 3000)

    def test_order_deletion(self):
        order = Order.objects.get(amount=1000)
        order.delete()
        self.assertFalse(Order.objects.filter(amount=1000).exists())

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(name="John Doe", phone="+254712345678")
        
        self.token = self.generate_jwt_token(self.customer)

        Order.objects.create(customer=self.customer, amount=1000, item="Book")
        Order.objects.create(customer=self.customer, amount=2000, item="Book")

    def generate_jwt_token(self, customer):
        payload = {
            "sub": str(customer.code),
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    def auth_headers(self):
        return {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

    def test_customer_list(self):
        response = self.client.get('/api/customers/', **self.auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_order_list(self):
        response = self.client.get('/api/orders/', **self.auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_order_create(self):
        response = self.client.post('/api/orders/', {'customer': self.customer.code, 'amount': 3000, 'item': 'Phone'}, **self.auth_headers())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 3)

    def test_order_delete(self):
        response = self.client.delete(f'/api/orders/{Order.objects.first().order_code}/', **self.auth_headers())
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Order.objects.count(), 1)
