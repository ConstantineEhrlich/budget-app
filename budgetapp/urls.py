from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index')
]

# Django authentication urs
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls'))
]