from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass
class posts(models.Model):
    usr=models.CharField(max_length=64)
    txt=models.CharField(max_length=6400)
    tmt=models.DateTimeField(default=datetime.now)
    likes=models.IntegerField(default=0)
    
    def serialize(self):
        return {
            "id": self.id,
            
            
            "txt": self.txt,
            "usr": self.usr,
            "tmt": self.tmt.strftime("%b %d %Y, %I:%M %p"),
             "likes":self.likes
             
        }
            
class profile(models.Model):
    usrs=models.CharField(max_length=64)
    following=models.CharField(max_length=64,null=True,blank=True)
    followers=models.CharField(max_length=64,null=True,blank=True)
class likes(models.Model):
   
    pid=models.IntegerField()
    by=models.CharField(max_length=64)
    def serialize1(self):
        return{
            
            "pid":self.pid,
            "by":self.by
        }
