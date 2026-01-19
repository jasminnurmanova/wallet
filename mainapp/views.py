from multiprocessing.managers import Value
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wallet, IncomeOutcome, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, F, DecimalField
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


@login_required
def home(request):
    wallets = Wallet.objects.filter(owner=request.user)
    histories = IncomeOutcome.objects.filter(author=request.user)

    total = sum(wallet.balance for wallet in wallets)

    income = (
        IncomeOutcome.objects
        .filter(author=request.user, type='income')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    outcome = (
        IncomeOutcome.objects
        .filter(author=request.user, type='outcome')
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


class TransactionView(LoginRequiredMixin, View):
    def get(self, request):
        wallet = Wallet.objects.filter(owner=request.user)
        categories = Category.objects.filter(type_p='expense')
        context = {
            'wallet': wallet,
            'categories': categories,
        }
        return render(request, 'transactions.html', context)

    def post(self, request):
        account_id = request.POST.get("account")
        category_id = request.POST.get("category")
        amount_raw = request.POST.get("amount")
        comment = request.POST.get("comment", "").strip()
        type_p = 'expense'

        try:
            wallet = Wallet.objects.get(id=account_id, owner=request.user)
        except Wallet.DoesNotExist:
            raise ValidationError(request, "Hisob topilmadi")

        try:
            category = Category.objects.get(id=category_id, type_p=type_p)
        except Category.DoesNotExist:
            raise ValidationError(request, "Kategoriya notogri")

        try:
            amount = Decimal(amount_raw)
            if amount <= 0:
                raise InvalidOperation
        except:
            raise ValidationError(request, "Summani togri kiriting")

        if wallet.balance > amount:
            wallet.balance -= amount
            wallet.save()
            Transaction.objects.create(
                author=request.user,
                account=account,
                category=category,
                amount=amount,
                type=type_p,
                comment=comment,
            )
            wallet.save()
        else:
            raise ValidationError(request, "Balansingiz yetarli emas")

        return redirect(reverse("finance:transaction"))


class AddWallet(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add-wallet.html')

    def post(self, request):
        title = request.POST.get("title")
        type_p = request.POST.get("type")
        balance = request.POST.get("balance")
        if not title:
            return render(request, "add-wallet.html", {
                "error": "Title is important"
            })

        Wallet.objects.create(
            owner=request.user,
            title=title,
            type=type_p,
            balance=balance
        )
        Transaction.objects.create(
            author=request.user,
            wallet=Wallet.objects.last(),
            category=Category.objects.filter(title__iexact='other').first(),
            amount=balance,
            type='income',
            comment="Added",
        )

        return redirect(reverse("main:wallet"))


# class History(LoginRequiredMixin, View):
#     def get(self, request):
#         qs = (Transaction.objects.filter(author=request.user).select_related("category", "account").order_by("-created"))
#
#         q = (request.GET.get("q") or "").strip()
#         tx_type = (request.GET.get("type") or "all").strip()
#         cat = (request.GET.get("cat") or "all").strip()
#         date_from = (request.GET.get("from") or "").strip()
#         date_to = (request.GET.get("to") or "").strip()
#
#         if q:
#             qs = qs.filter(
#                 Q(comment__icontains=q) |
#                 Q(category__title__icontains=q) |
#                 Q(account__title__icontains=q) |
#                 Q(amount__icontains=q)
#             )
#
#         if tx_type in ("income", "expense"):
#             qs = qs.filter(type=tx_type)
#
#         if cat != "all" and cat.isdigit():
#             qs = qs.filter(category_id=int(cat))
#
#         if date_from:
#             qs = qs.filter(created__date__gte=date_from)
#
#         if date_to:
#             qs = qs.filter(created__date__lte=date_to)
#
#         profit = (qs.aggregate(
#             income=Sum("amount", filter=Q(type="income")),
#             expense=Sum("amount", filter=Q(type="expense")),
#         ) or {})
#
#         income_sum = profit.get("income") or 0
#         expense_sum = profit.get("expense") or 0
#         profit_value = income_sum - expense_sum
#
#         categories = Category.objects.all().order_by("title")
#
#         context = {
#             "operations": qs,
#             "categories": categories,
#             "profit": profit_value,
#             "f_q": q,
#             "f_type": tx_type,
#             "f_cat": cat,
#             "f_from": date_from,
#             "f_to": date_to,
#         }
#         return render(request, "transactions.html", context)
#
#

class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        wallet = Wallet.objects.filter(owner=request.user)
        context = {
            'wallet': wallet,
        }
        return render(request, 'my-wallet.html', context)
