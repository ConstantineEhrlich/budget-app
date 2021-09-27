from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('test/', views.testview, name='testview')
]
