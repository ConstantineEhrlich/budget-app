from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('monthly/', views.MonthlyBudgetView.as_view(), name='monthly_budget'),
    path('monthly/<int:mon>', views.MonthlyBudgetView.as_view(), name='monthly_budget')
]
