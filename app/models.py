from django.db import models
import uuid
from django.utils import timezone
from users.models import User
import datetime

class Projet(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(null=False,max_length=50)
    description = models.TextField(null=True,blank=True)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)
    manger = models.ForeignKey(User, verbose_name=("Manager_proj"), on_delete=models.CASCADE,blank=True)
    
    def __str__(self):
        return self.name
    
class Tache(models.Model):
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('IN_PROGRESS', 'En cours'),
        ('COMPLETED', 'Terminée'),
        ('ON_HOLD', 'En suspens'),
        ('CANCELLED', 'Annulée'),
    ]
    
    id = models.AutoField(primary_key=True)
    titre = models.CharField(null=False, max_length=150)
    description = models.TextField(null=True,blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateField(null=True,blank=True)
    projet = models.ForeignKey(Projet, related_name='Taches', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='Taches', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    def __str__(self):
        return self.titre
    
    
