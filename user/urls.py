from .views import change_language,login,logout,SignupView,ProfileView,UpdateProfileView

from django.urls import path
app_name='users'

urlpatterns=[
    path('signup',SignupView.as_view(),name='signup'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('update/', UpdateProfileView.as_view(), name='update_profile'),
    path('change-language/', change_language, name='change_language'),
]
