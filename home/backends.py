from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from .models import Register

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, enrollment = None, password = None):
        try:
            user = Register.objects.get(enrollment = enrollment)
            if user.check_password(password):
                return user
        except Register.DoesNotExist:
            return None
    
    def get_user(self, enrollment):
        try:
            return Register.objects.get(pk = enrollment)
        except Register.DoesNotExist:
            return None