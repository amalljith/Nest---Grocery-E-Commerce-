from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save  


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=200)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_image",default="userimage.jpg")
    full_name = models.CharField(max_length=200, null=True,blank=True)
    bio = models.CharField(max_length=200, null=True,blank=True)
    phone = models.CharField(max_length=200, null=True,blank=True)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio}"
    


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.full_name


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=Users)
post_save.connect(save_user_profile, sender=Users)

