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

    total = sum(wallet.balance for wallet in wallets)

    income = (
        IncomeOutcome.objects
        .filter(user=request.user, type='income')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    outcome = (
        IncomeOutcome.objects
        .filter(user=request.user, type='outcome')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    total_transactions = income + outcome

    if total_transactions > 0:
        income_percentage = round((income / total_transactions) * 100)
        outcome_percentage = round((outcome / total_transactions) * 100)
    else:
        income_percentage = 0
        outcome_percentage = 0

    return render(request, 'index-2.html', {
        "total": total,
        "income": income,
        "outcome": outcome,
        "income_percentage": income_percentage,
        "outcome_percentage": outcome_percentage,
        "wallets": wallets,
        "histories": histories,
    })


@login_required
def transaction(request):
    user = request.user
    wallets = Wallet.objects.filter(user=user)
    categories = Category.objects.all()

    if request.method == "POST":
        wallet_id = request.POST.get("wallet")
        category_id = request.POST.get("category")
        trans_type = request.POST.get("type")
        amount = request.POST.get("amount")
        desc = request.POST.get("desc")
        currency = request.POST.get("currency")

        try:
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, "Amount must be greater than 0")
                return redirect("main:transaction")
        except:
            messages.error(request, "Invalid amount")
            return redirect("main:transaction")

        wallet = get_object_or_404(Wallet, id=wallet_id, user=user)
        category = get_object_or_404(Category, id=category_id)

        if trans_type == "outcome" and amount > wallet.balance:
            messages.error(request, "Not enough balance")
            return redirect("main:transaction")

        IncomeOutcome.objects.create(
            wallet=wallet,
            user=user,
            category=category,
            type=trans_type,
            amount=amount,
            desc=desc,
            currency=currency
        )

        if trans_type == "income":
            wallet.balance += amount
        else:
            wallet.balance -= amount

        wallet.save()

        messages.success(request, "Transaction saved successfully")
        return redirect("main:home")

    context = {
        "wallets": wallets,
        "categories": categories,
    }
    return render(request, "transactions.html", context)


@login_required
def create_wallet(request):
    if request.method == "POST":
        name = request.POST.get("name")
        wallet_type = request.POST.get("type")
        currency = request.POST.get("currency")
        balance = request.POST.get("balance")

        try:
            balance = Decimal(balance)
            if balance < 0:
                messages.error(request, "Balance cannot be negative")
                return redirect("create_wallet")
        except:
            messages.error(request, "Invalid balance")
            return redirect("create_wallet")

        if wallet_type == "visa" and currency == "UZS":
            messages.error(request, "VISA card cannot be in UZS currency")
            return redirect("create_wallet")

        Wallet.objects.create(
            user=request.user,
            name=name,
            type=wallet_type,
            currency=currency,
            balance=balance
        )

        return redirect("main:home")

    return render(request, "wallet_create.html")


def calender(request):
    return render(request,'calender.html')

@login_required
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