from django.urls import path
from .views import homeRequest, homePage, home, postRequest, addCustomer, getAllCustomers

urlpatterns = [
    # path('', homeRequest),
    # path('home', homePage),
    path('home', home),
    path('post-request', postRequest),
    path('add', addCustomer),
    path('all', getAllCustomers),
]