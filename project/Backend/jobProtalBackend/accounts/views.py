from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
# Create your views here.

@api_view(['GET'])
def healthChecker(request):
    return Response({
        "status" : "Working"
    })

@api_view(['POST'])
def registerUser(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        print(f"User saved successfully: {user.email}")
        
        return Response({
            "message": "User registered successfully",
            "user": serializer.data
        }, status=201) # 201 Created is better than 200
    
    # This is the part you were missing! 
    # It will tell you EXACTLY why it's failing (e.g., 'email already exists')
    print(f"Validation Errors: {serializer.errors}")
    return Response(serializer.errors, status=400)


# login

@api_view(['POST'])
def loginUser(request):
    print(request.data)
    
    serializer = LoginSerializer(data=request.data)
    
    print(f"login view login serializer {serializer}")
    if serializer.is_valid():
        user = serializer.validated_data
        print(f"inside is_valid() method {user}")
        print(f"refresh token for user : {RefreshToken.for_user(user)}")
        refreshtToken = RefreshToken.for_user(user)
        
        return Response({
            "accessToken": str(refreshtToken.access_token),
            "refreshToken": str(refreshtToken),
            "role": user.role
        })
        
    return Response(serializer.errors)