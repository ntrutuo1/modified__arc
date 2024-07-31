from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import SignUpForm
from .forms import ProfileForm
from .models import Profile


def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('log:home_page')
        else:
            context = {'form': form, 'error': 'Invalid username or password'}
            return render(request, 'login.html', context)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view (request):
    return redirect('log:login_page')

def render_home(request):
    return render(request, 'home.html')
@login_required
def render_main(request):
    return render(request, 'index.html')

def render_login(request):
    logout(request)
    return render(request, 'login.html')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "register.html"
    success_url = reverse_lazy("log:home_page")

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

@login_required
def profile(request):
    profile = request.user.profile 
    return render(request, 'profile.html', {'user': request.user, 'profile': profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('log:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})
