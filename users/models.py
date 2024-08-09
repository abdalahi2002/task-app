from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, nom=None, password=None, **extra_fields):
        
        if not email:
            raise ValueError('The email field must be set')

        email=self.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, nom=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user( email, nom, password, **extra_fields)
  

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    nom = models.CharField(null=False, max_length=70)
    email = models.EmailField(null=False,unique=True, max_length=254)
    password = models.CharField(max_length=128, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
       
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']
    
    objects = UserManager()
    
        
    def __str__(self):
        return self.nom
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    # def save(self,*args, **kwargs):
    #     if not self.pk :
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     # Do not hash the password here
    #     super().save(*args, **kwargs)

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)