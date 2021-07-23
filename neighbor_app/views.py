from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token

# Create your views here.
def signup_view(request):
  if request.method  == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.refresh_from_db()
      user.profile.first_name = form.cleaned_data.get('first_name')
      user.profile.last_name = form.cleaned_data.get('last_name')
      user.profile.email = form.cleaned_data.get('email')
      # user can't login until link confirmed
      user.is_active = False
      user.save()
      current_site = get_current_site(request)
      subject = 'Please Activate Your Account'
      # load a template like get_template() 
      # and calls its render() method immediately.
      message = render_to_string('activation_request.html', {
          'user': user,
          'domain': current_site.domain,
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          # method will generate a hash value with user related data
          'token': account_activation_token.make_token(user),
      })
      user.email_user(subject, message)
      return redirect('activation_sent')
  else:
    form = SignUpForm()
  return render(request, 'signup.html', {'form': form})
