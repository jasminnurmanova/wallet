from django.urls import path

from . import views
from .views import TransactionView, AddWallet, WalletView, AddCategory, History

app_name='main'

urlpatterns = [
    path('', views.home, name='home'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('wallet/', AddWallet.as_view(), name='wallet'),
    path('history/', History.as_view(), name='history'),
    path("wallet/add/",WalletView.as_view(), name="add_wallet"),
    path("category/add/",AddCategory.as_view(), name="add_category"),


]