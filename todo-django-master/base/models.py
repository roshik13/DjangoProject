from email.policy import default
import email
#from os import major
#from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete = models.CASCADE, null = True, blank=True
    )
    title = models.CharField(max_length= 200)
    description = models.TextField()
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    rewards=models.IntegerField(default=10)
    def __str__(self) :
        return self.title

    class Meta:
        ordering = ['complete'] 

class Pair(models.Model):
    user = models.ForeignKey(
        User, on_delete = models.CASCADE, null = True, blank=True
    )
    complete=models.IntegerField(default=0)
    upload=models.FileField(upload_to='uploads/')
    task=models.ForeignKey(
        Task,on_delete=models.CASCADE,null = True, blank=True
    )
    image = models.ImageField(upload_to="images", null=True)

class Inp(models.Model):
    upload=models.FileField(upload_to='uploads/')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rewards = models.IntegerField(default=0)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    #birth_date = models.DateField(null=True, blank=True)
    college = models.CharField(max_length=50, blank=True)
    major = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(default=1)
    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

