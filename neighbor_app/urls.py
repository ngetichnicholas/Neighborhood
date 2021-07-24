from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views as app_views
from django.contrib.auth import views as auth_views



urlpatterns = [
  path('admin/', admin.site.urls),
  path('', app_views.index, name="home"),
  path('signup/', app_views.signup_view, name="register"),
  path('sent/', app_views.activation_sent_view, name="activation_sent"),
  path('activate/<slug:uidb64>/<slug:token>/', app_views.activate, name='activate'),
  path('accounts/login/',app_views.login,name='login'),
  path('logout/',auth_views.LogoutView.as_view(template_name = 'registration/logout.html'),name='logout'),
  path('search',app_views.search,name='search'),
  path('create_neighborhood',app_views.create_neighborhood,name='create_neighborhood'),
  path('choose_neigborhood/<int:neighborhood_id>/',app_views.choose_neigborhood,name='choose_neighborhood'),
  path('leave_neigborhood/<int:neighborhood_id>/',app_views.leave_neigborhood,name='leave_neighborhood')

]