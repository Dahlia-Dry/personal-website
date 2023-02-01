from django.urls import path

from . import views

urlpatterns = [
    path('here/', views.home, name='home'),
    path('',views.redirect_home,name='redirect_home'),
    path('lost-in-space/', views.astrophoto_list.as_view(), name='space'),
    path('currently/', views.current_project_list.as_view(), name='current_projects'),
    path('in-lab-at-mit/',views.rle,name='rle'),
    path('taking-notes/',views.notes,name='notes'),
    path('in-new-places/',views.places,name='places'),
    path('thinking/',views.thinking,name='thinking'),
    path('outside/',views.outside,name='outside'),
    path('busy/',views.busy,name='busy'),
    path('at-work/',views.job,name='job')
] 