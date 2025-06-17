from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Welcome to Django Internship',
        'Thank you for registering!',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )