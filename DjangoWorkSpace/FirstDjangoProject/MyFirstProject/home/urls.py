from django.urls import path
from .views import homeRequest, homePage, home

urlpatterns = [
    # path('', homeRequest),
    # path('home', homePage),
    path('home', home),
]