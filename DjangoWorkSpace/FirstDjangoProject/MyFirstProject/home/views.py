from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CustomersSerializer, CustomerNameSerializer
from .models import Customers

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
    
@api_view(['POST'])
def postRequest(request):
    response = {
        "message" : "This is the response for post request"
    }
    
    return Response(response)

@api_view(['POST'])
def addCustomer(request):
    print(request.data)
    serializedData = CustomersSerializer(data = request.data)
    if serializedData.is_valid():
        serializedData.save()
    return Response({
        "message" : serializedData.data
    })
    
@api_view(['GET'])
def getAllCustomers(request):
    customers = Customers.objects.all()
    print(customers)
    serializedData = CustomerNameSerializer(customers, many=True)
    print(serializedData.data)
    return Response({
        'customers' : serializedData.data
    })