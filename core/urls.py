from django.urls import path

from . import views

urlpatterns = [
    path('here/', views.home, name='home'),
    path('',views.redirect_home,name='redirect_home'),
    path('currently/',views.currently,name='currently'),
    path('zoomin/',views.zoomin,name='zoomin'),
    path('in-new-places/',views.places,name='places'),
    path('thinking/',views.thinking,name='thinking'),
    path('learning/',views.learning,name='learning'),
    path('lost-in-space/',views.space,name='space'),
    path('outside/',views.outside,name='outside'),
    path('busy/',views.busy,name='busy'),
    path('looking-for-a-job/',views.job,name='job')
] 