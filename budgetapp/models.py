import csv
from django.db import models
from datetime import datetime

from django.db.models import Max, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.urls import reverse


# Once changes are done
# to this file, run the following in the terminal
#   $ python manage.py makemigrations budgetapp
# This will create a new migration script in ./budgetapp/migrations
# The script will have a number like '1234'. Run for this number:
#   $ python manage.py sqlmigrate budgetapp 1234
# This will generate sql code for the changes
# At last, run
#   $ python manage.py migrate


# TODO Add for_budget, for_year, for_month and for_category
# TODO Add abstract class "transaction" and then three inherited classes: Budget_Line, Outcome, Income
# TODO Add foreign key to Categories - budget
# TODO Add BooleanField() to Categories - income, expense, liability, budget - if the category applicable to this trans type
# TODO Add for_income, for_expense, for_liability, for_budget to the Category
# TODO update Budget_Line.save() so if the category is not open for expense or liability it will become open





# Create your models here.
class Transaction(models.Model):
    trns_types = [('exp', 'Expense'), ('lia', 'Liability'), ('inc', 'Income')]
    budget = models.ForeignKey('Budget', on_delete=models.PROTECT, to_field='code', verbose_name='Budget')
    trns_type = models.CharField(max_length=3, choices=trns_types, default='exp', verbose_name='Transaction Type')
    timestamp = models.DateTimeField(default=datetime.now(),
                                     # auto_now_add=True, # - disabled for migration
                                     verbose_name='Timestamp')
    year = models.PositiveSmallIntegerField(default=timezone.now().year, verbose_name='Year')
    month = models.PositiveSmallIntegerField(default=timezone.now().month, verbose_name='Month')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, to_field='code')
    user = models.CharField(max_length=3)
    #   user = models.ForeignKey(models.User, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    finalized = models.BooleanField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return self.timestamp.strftime("%-d-%b-%Y, %-H:%M:%S")

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])


class Budget_Line(models.Model):
    bdgt_types = [('bsl', 'Baseline'), ('spc', 'Special')]
    budget = models.ForeignKey('Budget', on_delete=models.PROTECT, to_field='code')
    bdgt_type = models.CharField(max_length=3, choices=bdgt_types, default='spc', verbose_name='Budget Type')
    timestamp = models.DateTimeField(default=datetime.now(),
                                     # auto_now_add=True, # - disabled for migration
                                     verbose_name='Timestamp')
    year = models.PositiveSmallIntegerField(default=timezone.now().year, verbose_name='Year')
    month = models.PositiveSmallIntegerField(default=timezone.now().month, verbose_name='Month')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, to_field='code')
    user = models.CharField(max_length=3)
    #   user = models.ForeignKey(models.User (model), on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'Budget Line'
        verbose_name_plural = 'Budget Lines'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])


class Budget(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=127, unique=True)

    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def get_current_month(self):
        current_month = Transaction.objects \
            .filter(trns_type='exp', budget=self.code) \
            .values('month').aggregate(month=Max('month'))
        return current_month['month']

    def get_monthly_values(self, category):
        result = []
        qset_bdgt = Budget_Line.objects.filter(budget=self).all()
        qset_trns = Transaction.objects.filter(budget=self).all()
        for mon in range(1, 13):
            monthly_values = {}
            baseline = qset_bdgt \
                .filter(bdgt_type='bsl', month__lte=mon, category=category) \
                .aggregate(Sum('amount'))['amount__sum']
            if baseline is None: baseline = 0
            special = qset_bdgt \
                .filter(bdgt_type='spc', month=mon, category=category) \
                .aggregate(Sum('amount'))['amount__sum']
            if special is None: special = 0
            tot_budget = baseline + special
            expenses = qset_trns \
                .filter(trns_type='exp', month=mon, category=category) \
                .aggregate(Sum('amount'))['amount__sum']
            if expenses is None: expenses = 0
            liabilities = qset_trns \
                .filter(trns_type='lia', month=mon, category=category) \
                .aggregate(Sum('amount'))['amount__sum']
            if liabilities is None: liabilities = 0
            tot_outcome = expenses + liabilities
            income = qset_trns \
                .filter(trns_type='inc', month=mon, category=category) \
                .aggregate(Sum('amount'))['amount__sum']
            if income is None: income = 0
            monthly_values['month'] = mon
            monthly_values['baseline'] = '{:,}'.format(baseline)
            monthly_values['special'] = '{:,}'.format(special)
            monthly_values['tot_budget'] = '{:,}'.format(tot_budget)
            monthly_values['expenses'] = '{:,}'.format(expenses)
            monthly_values['liabilities'] = '{:,}'.format(liabilities)
            monthly_values['tot_outcome'] = '{:,}'.format(tot_outcome)
            monthly_values['income'] = '{:,}'.format(income)
            result.append(monthly_values)
        return result

    def get_yearly_values(self):
        categories = Category.objects.all()
        yearly_values = []
        for cat in categories:
            monthly_values = {
                'category': cat.name,
                'values': self.get_monthly_values(cat)}
            yearly_values.append(monthly_values)
        return yearly_values


class Category(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=127, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.code)])


def import_csv_file(path_to_csv_file, target):
    # target can be 'bdgt', or 'trns'
    targets = ['bdgt', 'trns']
    if target not in targets:
        raise Exception('Target is incorrect')
    counter = 0
    imported_file = open(path_to_csv_file)
    csv_reader = csv.reader(imported_file)
    for row in csv_reader:
        counter = counter + 1
        if counter == 1:
            continue
        print('Importing line:', counter)

        params = {
            'budget': Budget.objects.get(code=str(row[0])),
            target + '_type': row[1],
            'timestamp': timezone.make_aware(datetime(int(row[2]), int(row[3]), int(row[4]), 12, 0, 0)),
            'year': int(row[2]),
            'month': int(row[3]),
            'category': Category.objects.get(name=row[5]),
            'user': row[6],
            'description': row[7],
            'amount': row[9]
        }
        if target == 'bdgt':
            new_trans = Budget_Line(**params)
        if target == 'trns':
            params['finalized'] = True
            new_trans = Transaction(**params)
        new_trans.save()


def refresh_data():
    Transaction.objects.all().delete()
    Budget_Line.objects.all().delete()
    imp_budgets = '/Users/constantine/Documents/Python/budget/modeling/imp_budgets.csv'
    imp_expenses = '/Users/constantine/Documents/Python/budget/modeling/imp_expenses.csv'
    imp_liabilities = '/Users/constantine/Documents/Python/budget/modeling/imp_liabilities.csv'
    import_csv_file(imp_budgets, 'bdgt')
    import_csv_file(imp_expenses, 'trns')
    import_csv_file(imp_liabilities, 'trns')


def get_monthly_expenses():
    # TODO move this logic into Budget class
    response = []
    qset = Transaction.objects.all()
    # run through categories
    for cat in Category.objects.filter(code__gt=10):
        result = {}
        sums = []
        for mon in range(1, 13):
            qry = qset.filter(category=cat, month=mon).aggregate(Sum('amount'))
            if qry['amount__sum'] == None:
                sums.append('-')
            else:
                num = '{:,}'.format(qry['amount__sum'])
                sums.append(num)
        result['name'] = cat.name
        result['sums'] = sums
        response.append(result)

    # calculate totals per category
    result = {}
    sums = []
    for mon in range(1, 13):
        qry = qset.filter(month=mon).aggregate(Sum('amount'))
        if qry['amount__sum'] == None:
            sums.append('-')
        else:
            num = '{:,}'.format(qry['amount__sum'])
            sums.append(num)
    result['name'] = 'Year Total'
    result['sums'] = sums
    response.append(result)
    return response
