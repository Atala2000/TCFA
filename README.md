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
    - body response structure:
    ```json
    [
    {
        "id": 1,
        "customer": 1,
        "item": "Product Name",
        "amount": 1,
        "time": "2021-01-01",
    }
    ]
    ```
* `POST api/orders/` - Create a new order
  - body request structure:
    ```json
    {
        "customer": "<customer_id>",
        "item": "Book",
        "amount": 100
    }
* `GET api/orders/?search=<id>/` - Get a single order
  - body response structure:
    ```json
    {
        "order_code": "<order_code>",
        "customer": "<customer_id>",
        "item": "book",
        "amount": "100",
        "time": "2024-07-23T10:58:23.705630Z"
    }
## Customer Endpoints
* `GET api/customers/` - Get a list of all customers
    - body response structure:
    ```json
    [
    {
        "id": 1,
        "name": "John Doe",
        "phone": "+00000",
    }
    ]
    ```
* `POST api/customers/` - Create a new customer
    - body request structure:
    ```json
    {
        "name": "John Doe",
        "phone": "+00000",
    }
    ```
* `GET api/customers/?search=<id>/` - Get a single customer
  - body response structure:
    ```json
    {
        "id": 1,
        "name": "John Doe",
        "phone": "+00000",
    }
    ```
