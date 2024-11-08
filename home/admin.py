from typing import Any
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import *

# Register your models here.

# Below code is added so that admin panel register user with password hashing
class RegisterAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        return super().save_model(request, obj, form, change)

admin.site.register(Register, RegisterAdmin)
admin.site.register(Attendance)
admin.site.register(KnownFace)