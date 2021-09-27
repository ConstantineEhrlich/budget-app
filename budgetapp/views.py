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
        'data': [{'name': 'Food', 'amount': 2977}, {'name': 'H&S', 'amount': 1225}]
    }
    return render(request, 'index.html', context=context)

def testview(request):

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
