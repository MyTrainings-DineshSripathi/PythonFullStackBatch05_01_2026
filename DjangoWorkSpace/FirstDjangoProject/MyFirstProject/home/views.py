from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import CustomersSerializer, CustomerNameSerializer
from .models import Customers

# Create your views here.

#CRUD

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False , methods=['GET'])
    def customer_by_email(self, request):
        email = request.GET.get('email')
        
        customer = Customers.objects.filter(email=email).first()
        print(customer)
        
        if not customer:
            return Response({
                "message" : "customer not found"
            })
        else:
            serializer = self.get_serializer(customer)
            return Response(serializer.data)
        
""" def homeRequest(request):
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
    }) """