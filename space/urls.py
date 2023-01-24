from django.urls import path
from django.conf import settings
from django.templatetags.static import static

from . import views

urlpatterns = [
    path('', views.photo_list.as_view(), name='space'),
    #path('',views.space,name='space'),
] 