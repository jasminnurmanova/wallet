from django.urls import path

from . import views
app_name='main'

urlpatterns = [
    path('', views.home, name='home'),
    path('transaction/', views.transaction, name='transaction'),
    path('calender/', views.calender, name='calender'),

    path('wallet/', views.wallet, name='wallet'),
    path('history/', views.history, name='history'),
    path("wallet/add/", views.add_wallet, name="add_wallet"),

]