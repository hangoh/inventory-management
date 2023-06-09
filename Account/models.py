from typing import Optional
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,name):
        user = self.model(name=name)
        user.save(using=self._db)
        return user

    def create_superuser(self,name):
        user = self.create_user(name=name)
        user.is_super = True
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name=models.CharField(unique=True, max_length=256, validators=[MinLengthValidator(1)])
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'name'

    objects = CustomUserManager()

    def __str__(self):
        return ("{}").format(self.name)
    
    def set_password(self, raw_password):
        pass

    def check_password(self, raw_password: str):
        return True
    def has_usable_password(self):
        return False