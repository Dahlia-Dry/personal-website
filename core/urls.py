from django.urls import path

from . import views

urlpatterns = [
    path('here/', views.index, name='index'),
    path('',views.redirect_home,name='redirect_home')
]