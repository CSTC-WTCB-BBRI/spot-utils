from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/hello-spot/',
            'method': 'GET',
            'body': None,
            'description': 'Hello, Spot!'
        },
    ]
    return JsonResponse(routes, safe=False)

def helloSpot(request):
    return HttpResponse('Hello, Spot!')