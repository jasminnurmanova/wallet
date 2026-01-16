from lib2to3.fixes.fix_input import context

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wallet, IncomeOutcome, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, F, DecimalField
from django.utils import timezone
from decimal import Decimal

from datetime import timedelta


@login_required
def home(request):
    wallets = Wallet.objects.filter(user=request.user)
    histories = IncomeOutcome.objects.filter(user=request.user)
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
        "wallets": wallets,
        "histories": histories
    })


@login_required
def transaction(request):
    user = request.user
    wallets = Wallet.objects.filter(user=user)
    categories = Category.objects.all()

    if request.method == "POST":
        wallet_id = request.POST.get("wallet")
        category_id = request.POST.get("category")
        type_ = request.POST.get("type")
        amount = request.POST.get("amount")
        desc = request.POST.get("desc")

        wallet = Wallet.objects.get(id=wallet_id, user=user)
        category = Category.objects.get(id=category_id)

        IncomeOutcome.objects.create(
            wallet=wallet,
            user=user,
            category=category,
            type=type_,
            amount=amount,
            desc=desc
        )
        return redirect("main:home")

    context = {
        "wallets": wallets,
        "categories": categories,
    }
    return render(request, "transactions.html", context)


@login_required
def add_wallet(request):
    if request.method == "POST":
        Wallet.objects.create(
            user=request.user,
            type=request.POST.get("type"),
            balance=request.POST.get("balance"),
            card_numbers=request.POST.get("card_numbers"),
            expire_date=request.POST.get("expire_date"),
        )
        return redirect("main:home")

    return render(request, "add-wallet.html")




def calender(request):
    return render(request,'calender.html')

def wallet(request):
    wallets = Wallet.objects.filter(user=request.user)
    total = 0
    for i in wallets:
        total += i.balance
    return render(request,'my-wallet.html', context={
        "total": total,
        "wallets": wallets
    })

@login_required
def history(request):
    period = request.GET.get("period", "week")
    now = timezone.now()

    if period == "day":
        start_date = now - timedelta(days=1)
    elif period == "month":
        start_date = now.replace(day=1)
    else:
        start_date = now - timedelta(days=7)

    histories = (
        IncomeOutcome.objects
        .filter(user=request.user, created_at__gte=start_date)
        .select_related("wallet", "category")
        .order_by("-created_at")
    )
    return render(request,'history.html', context={
        "histories":histories
    })