from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import logout, authenticate
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from .forms import *


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account is successfully created')
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})


class ProfileView(LoginRequiredMixin,View):
    login_url = '/account/login/'
    def get(self,request,username):
        user = get_object_or_404(CustomUser, username=username)
        return render(request, 'profile.html', {'user': user})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'registration/login.html')



class UpdateProfileView(View,LoginRequiredMixin):
    login_url='login'
    def get(self,request):
        form = UpdateProfileForm(instance=request.user)
        return render(request,'registration/update_profile.html',{'form':form})

    def post(self,request):
        form=UpdateProfileForm(instance=request.user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile',request.user)
        return render(request,'registration/update_profile',{'form':form})




@login_required
def change_language(request):
    lang = request.POST.get('language')

    if lang in ['en', 'uz']:
        request.user.language = lang
        request.user.save(update_fields=['language'])

    return redirect(request.META.get('HTTP_REFERER', '/'))