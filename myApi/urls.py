from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router=DefaultRouter()
router.register('contact_api',EmployeeViewSet)

urlpatterns=[
    path('',include(router.urls)),
    path('initiate_phonepe_payment/', Initiate_phonepe_payment.as_view(), name='initiate_phonepe_payment'),
    
]