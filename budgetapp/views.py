from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import *
from django.views import generic

from .models import *


# Create your views here.
def index(request):
    # context = Category.objects\
    # .filter(transaction__trns_type='exp', transaction__month=7)\
    # .values('name')\
    # .annotate(amount=Sum('transaction__amount'))

    context = {
        'expenses': get_monthly_expenses(),
        'periods': [
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
    }
    return render(request, 'index.html', context=context)


def test_request(request):
    context = {}
    context['variable'] = 'value'
    return HttpResponse(context)


class MonthlyBudgetView(generic.TemplateView):
    template_name = 'testview.html'

    def get_context_data(self, **kwargs):
        # TODO move this logic into Budget class and make it Budget.get_monthly_summary(self, month)
        # also, periods should be some kind of constant
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
        try:
            month = self.kwargs['mon']
        except KeyError:
            month = Budget.objects.get(code='2021').get_current_month()
        context = super().get_context_data()
        qset = Budget_Line.objects.all()
        # run through categories
        response = []
        for cat in Category.objects.filter(code__gt=10):
            baseline = special = total = 0
            baseline = qset.filter(bdgt_type='bsl', month__lte=month, category=cat).aggregate(Sum('amount'))['amount__sum']
            if baseline is None: baseline = 0
            special = qset.filter(bdgt_type='spc', month=month, category=cat).aggregate(Sum('amount'))['amount__sum']
            if special is None: special = 0
            result = {}
            result['catname'] = cat.name
            result['baseline'] = '{:,}'.format(baseline)
            result['special'] = '{:,}'.format(special)
            result['total'] = '{:,}'.format(baseline + special)
            response.append(result)
        result = {}
        baseline = special = total = 0
        baseline = qset.filter(bdgt_type='bsl', month__lte=month).aggregate(Sum('amount'))['amount__sum']
        if baseline is None: baseline = 0
        special = qset.filter(bdgt_type='spc', month=month).aggregate(Sum('amount'))['amount__sum']
        if special is None: special = 0
        result['catname'] = 'Total'
        result['baseline'] = '{:,}'.format(baseline)
        result['special'] = '{:,}'.format(special)
        result['total'] = '{:,}'.format(baseline + special)
        response.append(result)
        context['budget'] = response
        context['month'] = periods[month - 1]
        context['periods'] = periods
        return context


class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'expenses'

    def get_queryset(self):
        budget = Budget.objects.get(code='2021')
        current_month = budget.get_current_month()
        return Category.objects \
            .filter(transaction__trns_type='exp', transaction__month__exact=current_month) \
            .annotate(amount=Sum('transaction__amount')) \
            .values('name', 'transaction__month', 'amount')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budgets = Category.objects \
            .annotate(amount=Sum('budget_line__amount')) \
            .values('name', 'amount')
        context['budgets'] = budgets
        return context
