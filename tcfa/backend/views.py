from django.http import JsonResponse

def index(request):
    return JsonResponse({
        "message": "Welcome to an Order API service",
        "endpoints": {
            "/api/customers": "Get a list of customers",
            "/api/orders": "Get a list of orders",
            "/user/auth/login": "Authenticate and login",
            "/user/auth/logout": "Logout and end session"
        }
    })
