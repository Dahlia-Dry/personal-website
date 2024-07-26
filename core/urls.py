from django.urls import path,re_path
import json
import copy
from core.models import *
from django.conf import settings

from . import views

MENU= json.loads(open(os.path.join(settings.STATIC_ROOT,'assets/here/menu.json')).read())

root_views = ['here','in-the-news','lost-in-space','at-work','on-a-bike']
list_views = ['researching','making','working','in-new-places']
detail_views = ['researching','making','on-a-bike','working','at-work','in-new-places']


home_patterns = [path('',views.redirect_home,name='redirect_home'),
                 path('here/',views.redirect_home,name='here/')]

root_view_patterns = [path(f"{r}",views.root_view,name=f"{r}") for r in root_views]

list_view_patterns = [path(f"{l}",views.list_view,name=f"{l}_post_list") for l in list_views]

detail_view_patterns = [path(f"{d}/<slug>",views.detail_view,name=f"{d}_post_detail") for d in detail_views]

currently_patterns = [path(f"currently",views.current_view,name=f"current_post_list")]

urlpatterns= home_patterns+root_view_patterns+list_view_patterns+detail_view_patterns+currently_patterns