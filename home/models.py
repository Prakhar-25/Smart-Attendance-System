from django.db import models
from django.contrib.auth.hashers import make_password
import pickle
import numpy as np

class Register(models.Model):
    enrollment = models.CharField(max_length=25, blank = False,unique = True)
    name = models.CharField(max_length=70, blank = False)
    mobile = models.CharField(max_length=20, blank = False)
    email = models.EmailField(max_length = 100, blank = False)
    branch = models.CharField(max_length = 100)
    img = models.ImageField(upload_to='registered_users/')
    password = models.CharField(max_length=128)  # 128 is the recommended length for hashed passwords

    def save_user(self,*args, **kwargs):
        self.password = make_password(self.password)
        super(Register,self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Register, on_delete= models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default = False)

    class Meta:
        unique_together = ('student','date')  # to prevent duplicate record on same date by same user

    def __str__(self) -> str:
        return f"{self.student.name} - {self.date} - {'Present' if self.is_present else 'Absent'}"
    
class KnownFace(models.Model):
    # to store known names and encodings for face recognition
    known_name = models.CharField(max_length=70)
    known_encoding = models.BinaryField()  # encodings will be converted to binary

    def save_encoding(self,encoding_array):
        self.known_encoding = pickle.dumps(encoding_array)  # convert to binary
        self.save()

    def get_encoding(self):
        return pickle.loads(self.known_encoding)

    def __str__(self):
        return self.known_name