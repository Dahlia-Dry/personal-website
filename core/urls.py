from django.urls import path,re_path

from . import views

urlpatterns = [
    path('taking-notes/',views.notes,name='notes'),
    path('in-new-places/',views.places,name='places'),
    path('thinking/',views.thinking,name='thinking'),
    path('outside/',views.outside,name='outside'),
] 

home_patterns = [path('here/', views.home, name='home'),
                 path('',views.redirect_home,name='redirect_home')]

list_view_patterns = [path('lost-in-space/', views.astrophoto_list.as_view(), name='space'),
                      path('currently/', views.create_list_view([6]).as_view(), name='current_projects'),
                      path('busy/',views.create_list_view([0,6]).as_view(),name='projects'),
                      ]

detail_view_patterns = [path('busy/<slug>',views.create_detail_view(0),name='busy_detail'),
                        path('currently/<slug>',views.create_detail_view(6),name='currently_detail'),
                        path('at-work/',views.job,name='job')]

urlpatterns= home_patterns+list_view_patterns+detail_view_patterns