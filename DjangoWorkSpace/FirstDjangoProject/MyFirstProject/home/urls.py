from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import homeRequest, homePage, home, postRequest, addCustomer, getAllCustomers, CustomerViewSet
from .views import CustomerViewSet
router = DefaultRouter()
router.register('customer', CustomerViewSet)

urlpatterns = [
    # path('', homeRequest),
    # path('home', homePage),
    # path('home', home),
    # path('post-request', postRequest),
    # path('add', addCustomer),
    # path('all', getAllCustomers),
    path('', include(router.urls))
]