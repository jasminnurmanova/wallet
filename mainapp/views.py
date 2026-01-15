from lib2to3.fixes.fix_input import context
from django.db.models import Sum


from django.shortcuts import render
from .models import Wallet, IncomeOutcome, Category


def home(request):
    wallets = Wallet.objects.all()
    total = 0
    for i in wallets:
        total+=i.balance

    result1 = IncomeOutcome.objects.filter(type='income').aggregate(total=Sum('amount'))
    income = result1['total'] or 0

    result2 = IncomeOutcome.objects.filter(type='outcome').aggregate(total=Sum('amount'))
    outcome = result2['total'] or 0
    return render(request, 'index-2.html', context={
        "total":total,
        "income": income,
        "outcome": outcome,
        "wallets": wallets
    })


def transaction(request):
    wallets = Wallet.objects.all()
    categories = Category.objects.all()
    return render(request, 'transactions.html', context={
        "wallets": wallets,
        "categories": categories
    })