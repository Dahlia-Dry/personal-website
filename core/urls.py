from django.urls import path,re_path
import json
import copy
from core.models import *
from django.conf import settings

from . import views

MENU= json.loads(open(os.path.join(settings.STATIC_ROOT,'assets/here/menu.json')).read())

list_views = ['currently','researching','on-a-bike']
detail_views = ['currently','researching','making','on-a-bike']


home_patterns = [path('',views.redirect_home,name='redirect_home'),
                 path('here',views.home_view,name='here'),
                 path('here/',views.redirect_home,name='here/')]

list_view_patterns = [path(f"{l}",views.list_view,name=f"{l}_post_list") for l in list_views]

detail_view_patterns = [path(f"{d}/<slug>",views.detail_view,name=f"{d}_post_detail") for d in detail_views]

astro_patterns = [path('lost-in-space',views.astrophoto_gallery,name='astrophoto')] + [path(f'lost-in-space/{a.uid}',views.astrophoto_indiv,name=f'astro_{a.uid}') for a in AstroPhoto.objects.all()]
urlpatterns= home_patterns+list_view_patterns+detail_view_patterns+astro_patterns