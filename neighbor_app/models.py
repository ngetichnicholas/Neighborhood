from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100, blank=True)
  last_name = models.CharField(max_length=100, blank=True)
  email = models.EmailField(max_length=150)
  signup_confirmation = models.BooleanField(default=False)
  bio =models.TextField(null=True)
  profile_picture =CloudinaryField('image')
  neighborhood = models.ForeignKey('NeighborHood', on_delete=SET_NULL,null=True, related_name='members', blank=True)
  location =models.CharField(max_length=60,blank=True,null=True)

  def __str__(self):
    return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
  if created:
      Profile.objects.create(user=instance)
  instance.profile.save()
  

class NeighborHood(models.Model):
  name = models.CharField(max_length=60)
  location = models.CharField(max_length=60)
  admin = models.ForeignKey(Profile,on_delete=CASCADE,related_name='hood')
  description = models.TextField()
  population = models.ImageField(null=True,blank = True)
  police_count = models.ImageField(null=True,blank = True)
  hospital_caunt = models.ImageField(null=True,blank = True)

  def create_neighborhood(self):
    self.save()

  def delete_neighborhood(self):
    self.delete()

  @classmethod
  def get_neighborhood(cls, neighborhood_id):
    return cls.objects.filter(id=neighborhood_id)
  
  def __str__(self):
    return f'{self.name} hood'


class Post(models.Model):
  title = models.CharField(max_length=144)
  post = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User,on_delete=CASCADE,related_name='owner')
  neighborhood = models.ForeignKey(NeighborHood,on_delete=CASCADE,related_name='neighborhood_post')

  def save_post(self):
    self.save()

  def delete_post(self):
    self.delete()

  @classmethod
  def show_posts(cls):
    posts = cls.objects.all()
    return posts

  def __str__(self):
    return self.title


class Business(models.Model):
  name =models.CharField(max_length=60)
  description = models.TextField()
  neighborhood = models.ForeignKey(NeighborHood,on_delete=CASCADE,related_name='business')
  user = models.ForeignKey(User,on_delete=CASCADE,related_name='user')
  email = models.EmailField()

  def create_business(self):
    self.save()

  def delete_business(self):
    self.delete()

  @classmethod
  def search_business(cls, name):
    return cls.objects.filter(name__icontains=name).all()

  def __str__(self):
    return f'{self.name} Business'