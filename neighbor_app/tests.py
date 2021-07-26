# Create your tests here.
from neighbor_app.views import neighborhood
from django.test import TestCase
from .models import Business,Profile,NeighborHood,Post
from django.contrib.auth.models import User


class BusinessTest(TestCase):
  def setUp(self):
    self.user = User.objects.create(id=1, username='NgetichNIck')
    self.neighborhood = NeighborHood.objects.create(id=1, name='home')
    self.busines = Business.objects.create(id=1, name='Moringa business', description='Moringa business description',image='https://cloudinary url',created_at='2021,6,26',updated_at='2021,6,26', neighborhood=self.neighborhood,user=self.user,email='nick@gmail.com')

  def test_instance(self):
    self.assertTrue(isinstance(self.busines, Business))

  def test_create_business(self):
    self.busines.create_business()
    business = Business.objects.all()
    self.assertTrue(len(business) > 0)

  def test_get_business(self, id):
    self.business.save()
    business = Business.get_businesss(post_id=id)
    self.assertTrue(len(business) == 1)

class TestProfile(TestCase):
  def setUp(self):
    self.user = User(id=1, username='NgetichNick', password='Moringa')
    self.user.save()

  def test_instance(self):
    self.assertTrue(isinstance(self.user, User))

  def test_save_user(self):
    self.user.save()

  def test_delete_user(self):
    self.user.delete()

