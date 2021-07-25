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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.core.mail import EmailMessage
from .models import Profile,NeighborHood,Post,Business
from .forms import CreateNeighborHoodForm,CreateBusinessForm,CreatePostForm,UpdateBusinessForm


# Create your views here.
@login_required
def index(request):
  neighborhoods = NeighborHood.objects.all().order_by('-created_at')
  return render(request, 'index.html',{'neighborhoods':neighborhoods})

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
      message = render_to_string('registration/activation_request.html', {
          'user': user,
          'domain': current_site.domain,
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          # method will generate a hash value with user related data
          'token': account_activation_token.make_token(user),
      })
      to_email = form.cleaned_data.get('email')
      email = EmailMessage(subject, message, to=[to_email])
      email.send()
      return redirect('activation_sent')
  else:
    form = SignUpForm()
  return render(request, 'registration/signup.html', {'form': form})

def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        auth_login(request, user)
        messages.info(request, f"You are now logged in as {username}")
        return redirect('home')
      else:
        messages.error(request, "Invalid username or password.")
    else:
      messages.error(request, "Invalid username or password.")
  form = AuthenticationForm()
  return render(request = request,template_name = "registration/login.html",context={"form":form})

def activation_sent_view(request):
  return render(request, 'registration/activation_sent.html')

def activate(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  # checking if the user exists, if the token is valid.
  if user is not None and account_activation_token.check_token(user, token):
    # if valid set active true 
    user.is_active = True
    # set signup_confirmation true
    user.profile.signup_confirmation = True
    user.save()
    login(request)
    return redirect('login')
  else:
    return render(request, 'registration/activation_invalid.html')

@login_required
def search(request):
  if 'business' in request.GET and request.GET["business"]:
    search_term = request.GET.get("business")
    searched_business = Business.objects.filter(name__icontains=search_term).all()
    message = f"{search_term}"

    return render(request,'search.html', {"message":message,"businesss":searched_business})

  else:
    message = "You haven't searched for any term"
    return render(request,'search.html',{"message":message})

@login_required
def create_neighborhood(request):
  if request.method == 'POST':
    add_neighborhood_form = CreateNeighborHoodForm(request.POST, request.FILES)
    if add_neighborhood_form.is_valid():
      neighborhood = add_neighborhood_form.save(commit=False)
      neighborhood.admin = request.user.profile
      neighborhood.save()
      return redirect('home')
  else:
    add_neighborhood_form = CreateNeighborHoodForm()
  return render(request, 'create_neighborhood.html', {'add_neighborhood_form': add_neighborhood_form})

def choose_neighborhood(request, neighborhood_id):
  neighborhood = get_object_or_404(NeighborHood, id=neighborhood_id)
  request.user.profile.neighborhood = neighborhood
  request.user.profile.save()
  return redirect('home')

def get_neighborhood_users(request, neighborhood_id):
  neighborhood = NeighborHood.objects.get(id=neighborhood_id)
  users = Profile.objects.filter(neighborhood=neighborhood)
  return render(request, 'neighborhood_users.html', {'users': users})

def leave_neighborhood(request, neighborhood_id):
  neighborhood = get_object_or_404(NeighborHood, id=neighborhood_id)
  request.user.profile.neighborhood = None
  request.user.profile.save()
  return redirect('home')

@login_required
def create_business(request,neighborhood_id):
  neighborhood = NeighborHood.objects.get(id=neighborhood_id)
  if request.method == 'POST':
    add_business_form = CreateBusinessForm(request.POST, request.FILES)
    if add_business_form.is_valid():
      business = add_business_form.save(commit=False)
      business.neighborhood =neighborhood
      business.user = request.user
      business.save()
      return redirect('neighborhood', neighborhood.id)
  else:
    add_business_form = CreateBusinessForm()
  return render(request, 'create_business.html', {'add_business_form': add_business_form,'neighborhood':neighborhood})

def create_post(request, neighborhood_id):
  neighborhood = NeighborHood.objects.get(id=neighborhood_id)
  if request.method == 'POST':
    add_post_form = CreatePostForm(request.POST)
    if add_post_form.is_valid():
      post = add_post_form.save(commit=False)
      post.neighborhood = neighborhood
      post.user = request.user
      post.save()
      return redirect('neighborhood', neighborhood.id)
  else:
    add_post_form = CreatePostForm()
  return render(request, 'create_post.html', {'add_post_form': add_post_form,'neighborhood':neighborhood})

def neighborhood(request, neighborhood_id):
  current_user = request.user
  neighborhood = NeighborHood.objects.get(id=neighborhood_id)
  business = Business.objects.filter(neighborhood=neighborhood)
  posts = Post.objects.filter(neighborhood=neighborhood)

  return render(request, 'neighborhood.html', {'current_user':current_user, 'neighborhood':neighborhood,'business':business,'posts':posts})

@login_required
def delete_business(request,business_id):
  current_user = request.user
  business = Business.objects.get(pk=business_id)
  if business:
    business.delete_business()
  return redirect('home')

@login_required
def update_business(request, business_id):
  business = Business.objects.get(pk=business_id)
  if request.method == 'POST':
    update_business_form = UpdateBusinessForm(request.POST, instance=business)
    if update_business_form.is_valid():
      update_business_form.save()
      messages.success(request, f'Business updated!')
      return redirect('home')
  else:
    update_business_form = UpdateBusinessForm(instance=business)

  return render(request, 'update_business.html', {"update_business_form":update_business_form})
