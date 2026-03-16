from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

def homeRequest(request):
    print(request)
    return HttpResponse("This is my first Response")

def homePage(request):
    return render(request, "index.html")

@api_view(['GET'])
def home(request):
    return Response({
        "message" : "Hello"
    })