from django.contrib import admin
from .models import Wallet, IncomeOutcome

admin.site.register([Wallet, IncomeOutcome])
# Register your models here.
