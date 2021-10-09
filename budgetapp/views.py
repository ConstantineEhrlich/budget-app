# TODO Implement User Model and add Login, Register, etc
# TODO Create ListView, DetiailView, AddView for each model: Budget, Budget_Line, Outcome, Income, Category


from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import *

periods = [
    {'num': 1, 'long_name': 'January', 'short_name': 'Jan'},
    {'num': 2, 'long_name': 'February', 'short_name': 'Feb'},
    {'num': 3, 'long_name': 'March', 'short_name': 'Mar'},
    {'num': 4, 'long_name': 'April', 'short_name': 'Apr'},
    {'num': 5, 'long_name': 'May', 'short_name': 'May'},
    {'num': 6, 'long_name': 'June', 'short_name': 'Jun'},
    {'num': 7, 'long_name': 'July', 'short_name': 'Jul'},
    {'num': 8, 'long_name': 'August', 'short_name': 'Aug'},
    {'num': 9, 'long_name': 'September', 'short_name': 'Sep'},
    {'num': 10, 'long_name': 'October', 'short_name': 'Oct'},
    {'num': 11, 'long_name': 'November', 'short_name': 'Nov'},
    {'num': 12, 'long_name': 'December', 'short_name': 'Dec'}
]


# Create your views here.
def index(request):

    context = {
        'test': 'It works!'
    }
    return render(request, 'index.html', context=context)




# class TransactionEntryView(LoginRequiredMixin, generic.CreateView):
#     model = Transaction
#     template_name = 'transaction_entry.html'
#     fields = ['budget',
#               'trns_type',
#               'year',
#               'month',
#               'user',
#               'category',
#               'description',
#               'finalized',
#               'amount']
#
#
# class MonthlyBudgetView(LoginRequiredMixin, generic.TemplateView):
#     template_name = 'month_view.html'
#
#     def get_context_data(self, **kwargs):
#         # also, periods should be some kind of constant
#         bdg = Budget.objects.get(code='2021')
#         try:
#             month = self.kwargs['mon']
#         except KeyError:
#             month = bdg.get_current_month()
#         context = super().get_context_data()
#         context['periods'] = periods
#         context['month'] = month
#         context['data'] = bdg.get_yearly_values()
#
#         return context
#
#
# class CategoryListView(generic.ListView):
#     model = Category
#     context_object_name = 'expenses'
#
#     def get_queryset(self):
#         budget = Budget.objects.get(code='2021')
#         current_month = budget.get_current_month()
#         return Category.objects \
#             .filter(transaction__trns_type='exp', transaction__month__exact=current_month) \
#             .annotate(amount=Sum('transaction__amount')) \
#             .values('name', 'transaction__month', 'amount')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         budgets = Category.objects \
#             .annotate(amount=Sum('budget_line__amount')) \
#             .values('name', 'amount')
#         context['budgets'] = budgets
#         return context
