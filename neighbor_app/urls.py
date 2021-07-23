from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views as app_views
urlpatterns = [
  path('admin/', admin.site.urls),
  path('', app_views.index, name="home"),
  path('signup/', app_views.signup_view, name="register"),
  path('sent/', app_views.activation_sent_view, name="activation_sent"),
  path('activate/<slug:uidb64>/<slug:token>/', app_views.activate, name='activate'),
]