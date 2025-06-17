from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import send_welcome_email


# Create your views here.
@api_view(['GET'])
def public_endpoint(request):
    return Response({"message": "This is a public endpoint."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_endpoint(request):
    return Response({"message": "This is a protected endpoint."})

@api_view(['POST'])
def register_user(request):
    user_email = request.data.get('email')
    send_welcome_email.delay(user_email)
    return Response({"message": "User registered. Welcome email sent."})
