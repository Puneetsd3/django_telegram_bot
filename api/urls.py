from django.urls import path
from .views import public_endpoint, protected_endpoint

urlpatterns = [
    path('public/', public_endpoint),
    path('protected/', protected_endpoint),
]