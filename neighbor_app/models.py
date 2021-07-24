from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


# Create your models here.
class NeighborHood(models.Model):
  pass

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100, blank=True)
  last_name = models.CharField(max_length=100, blank=True)
  email = models.EmailField(max_length=150)
  signup_confirmation = models.BooleanField(default=False)
  bio =models.TextField(null=True)
  profile_picture =CloudinaryField('image')
  neighborhood = models.ForeignKey(NeighborHood, on_delete=SET_NULL,null=True, related_name='members', blank=True)
  location =models.CharField(max_length=60,blank=True,null=True)

  def __str__(self):
    return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
  if created:
      Profile.objects.create(user=instance)
  instance.profile.save()
