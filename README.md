# Django Order API Service
This is a simple Django API service that allows you to create, read, update and delete orders. It is a simple REST API service that uses Django Rest Framework.

## Installation
```bash
git clone https://github.com/Atala2000/TCFA.git
cd TCFA
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 80000
```

## Usage
You can use the following endpoints to interact with the API service:
* JWT Token is needed for access to endpoints, to get one go to /user/auth/login in browser and enter your credentials
* For subsequent requests pass the token in the Authorization header as follows: `
* `Authorization : Bearer <token here>`

## Order Endpoints
* `GET api/orders/` - Get all orders
* `POST api/orders/` - Create a new order
* `GET api/orders/?search=<id>/` - Get a single order
  
## Customer Endpoints
* `GET api/customers/` - Get all customers
* `POST api/customers/` - Create a new customer
* `GET api/customers/?search=<id>/` - Get a single customer