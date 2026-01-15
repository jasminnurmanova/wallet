from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import CustomUser

# Create your views here.


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)

            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']

            user.save()
            messages.success(request, 'Your account is successfully created')
            return redirect('login')

        return render(request, 'registration/signup.html', {'form': form})

class ProfileView(LoginRequiredMixin,View):
    login_url = '/account/login/'
    def get(self,request,username):
        user = get_object_or_404(CustomUser, username=username)
        return render(request, 'profile.html', {'customuser': user})


class UpdateProfileView(View,LoginRequiredMixin):
    login_url='login'
    def get(self,request):
        form = UpdateProfileForm(instance=request.user)
        return render(request,'profile_update.html',{'form':form})

    def post(self,request):
        form=UpdateProfileForm(instance=request.user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile',request.user)
        return render(request,'update_profile',{'form':form})