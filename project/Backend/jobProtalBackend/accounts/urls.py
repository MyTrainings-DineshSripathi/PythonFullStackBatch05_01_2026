from django.urls import path, include
from .views import registerUser, healthChecker, loginUser

urlpatterns = {
    path('health', healthChecker),
    path('register', registerUser),
    path('login', loginUser)
}