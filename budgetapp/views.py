from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import *
from django.views import generic
from .models import *


# Create your views here.
def index(request):
    #context = Category.objects\
        #.filter(transaction__trns_type='exp', transaction__month=7)\
        #.values('name')\
        #.annotate(amount=Sum('transaction__amount'))



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

def testview(request):
    context = Context()
    return render(request, 'index.html', context=context)

class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'expenses'

    def get_queryset(self):
        return Category.objects \
            .filter(transaction__trns_type='exp') \
            .annotate(amount=Sum('transaction__amount')) \
            .values('name', 'transaction__month', 'amount')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budgets = Category.objects \
            .annotate(amount=Sum('budget_line__amount')) \
            .values('name', 'amount')
        context['budgets'] = budgets
        return context
