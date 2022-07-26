from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your models here.

#Signals for user specific token
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)


class DatabaseConnection(models.Model):
    name=models.CharField(max_length=100)
    creationUser=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    creationTime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    lastUpdatedUser=models.CharField(max_length=100,null=True,blank=True)
    lastUpdateTime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    parameter=models.FileField(upload_to="uploads/dbconnection",null=True,blank=True)
    
    @property
    def creation_user(self):
        if self.creationUser:
            return self.creationUser.username
        
    def __str__(self):
        return self.name

    
class DataModel(models.Model):
    name=models.CharField(max_length=100)
    creationUser=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    creationTime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    lastUpdatedUser=models.CharField(max_length=100,null=True,blank=True)
    lastUpdateTime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    parameter=models.FileField(upload_to="uploads/datamodels",null=True,blank=True)

    def __str__(self):
        return self.name
    
    @property
    def creation_user(self):
        if self.creationUser:
            return self.creationUser.username
    
    
class DataSource(models.Model):
    name=models.CharField(max_length=100)
    creationUser=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    creationTime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    lastUpdatedUser=models.CharField(max_length=100,null=True,blank=True)
    lastUpdateTime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    parameter=models.FileField(upload_to="uploads/datasource",null=True,blank=True)
    # sql_file=models.FileField(upload_to="uploads/sql_file",null=True,blank=True)
    # data_model=models.ForeignKey(DataModel,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def creation_user(self):
        if self.creationUser:
            return self.creationUser.username
    
    
class Explorer(models.Model):
    name=models.CharField(max_length=100)
    creationUser=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    creationTime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    lastUpdatedUser=models.CharField(max_length=100,null=True,blank=True)
    lastUpdateTime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    parameter=models.FileField(upload_to="uploads/explorer",null=True,blank=True)

    def __str__(self):
        return self.name
    
    @property
    def creation_user(self):
        if self.creationUser:
            return self.creationUser.username
    
    
    
    