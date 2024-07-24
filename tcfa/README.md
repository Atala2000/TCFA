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
* JWT Token is needed for access to endpoints, to get one go to `http://localhost:8000/user/auth/login` in browser and enter your credentials
* The response will be a json object with the token inside
  ```json
  {
  "message": "Authentication successful",
  "token": {
    "access_token": "<value>",
    "id_token": "<value>",
    "scope": "openid profile email",
    "expires_in": 86400,
    "token_type": "Bearer",
    "expires_at": 1721825073,
    "userinfo": {
      "given_name": "John",
      "family_name": "Doe",
      "nickname": "John",
      "name": "John Doe",
      "picture": "https://lh3.googleusercontent.com/<value>",
      "updated_at": "2024-07-23T08:05:32.520Z",
      "email": "johndoe@gmail.com",
      "email_verified": true,
      "iss": "xxx",
      "aud": "5xmDDP713kDbXQLAJmYHbrsEUycwkTSh",
      "iat": 1721738673,
      "exp": 1721774673,
      "sub": "xxx",
      "nonce": "xxx"
    }
  }
  ```
* For subsequent requests pass the `id_token` in the Authorization header as follows: `
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

### Africa Talks
* Once an order is posted a message is sent to the Africa Talks API
* 