from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('monthly/', views.MonthlyBudgetView.as_view(), name='monthly_budget'),
    path('monthly/<int:mon>', views.MonthlyBudgetView.as_view(), name='monthly_budget'),
    path('monthly/<int:mon>', views.MonthlyBudgetView.as_view(), name='model-detail-view')
]

# Django authentication urs
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls'))
]

# Data input forms
urlpatterns += [
    path('transaction_entry/', views.TransactionEntryView.as_view(), name='transaction_entry')
]