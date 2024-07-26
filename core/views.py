from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
import copy
from django.conf import settings

import sys
sys.path.append('..')
from utilities.webpage import *

MENU= json.loads(open(os.path.join(settings.STATIC_ROOT,'assets/here/menu.json')).read())
if settings.DEBUG:
    host='http://127.0.0.1:8000' #localhost
else:
    host='https://www.dahlia.is'
base_context = {'menu':MENU,'hostname':host}

def redirect_home(request):
    response = redirect('/here')
    return response

def root_view(request):
    context =copy.deepcopy(base_context)
    if not request.path.endswith('/'):
        post_type = request.path.split('/')[-1]
    else:
        post_type = request.path.split('/')[-2]
    context["post"] = Post.objects.get(slug=post_type)
    post_data = webPage(context['post'].content)
    template_dir = os.path.split(post_data.meta['html'])
    template_name = os.path.join(template_dir[0].split('/')[-1],template_dir[1])
    context["header_content"] = post_data.meta['post_type']
    for key in post_data.content:
        context[key] = post_data.content[key]
    return render(request, template_name, context)

def custom_404(request, exception):
    context=copy.deepcopy(base_context)
    context["header_content"] = 'lost?'
    return render(request, 'pages_html/404.html', context=context,status=404)

def custom_500(request, exception):
    context=copy.deepcopy(base_context)
    context["header_content"] = 'lost?'
    return render(request, 'pages_html/404.html', context=context,status=500)

def astrophoto_gallery(request):
    queryset = AstroPhoto.objects.all()
    template_name = 'pages_html/lost-in-space.html'
    context = copy.deepcopy(base_context)
    context['photo_list'] = queryset
    context['header_content'] = 'lost-in-space'
    return render(request,template_name,context)

def detail_view(request,slug):
    if not request.path.endswith('/'):
        slug = request.path.split('/')[-1]
    else:
        slug = request.path.split('/')[-2]
    context =copy.deepcopy(base_context)
    context["post"] = Post.objects.get(slug=slug)
    post_data = webPage(context['post'].content)
    template_dir = os.path.split(post_data.meta['html'])
    template_name = os.path.join(template_dir[0].split('/')[-1],template_dir[1])
    context["header_content"] = post_data.meta['post_type']
    for key in post_data.content:
        context[key] = post_data.content[key]
    return render(request, template_name, context)

def list_view(request):
    if not request.path.endswith('/'):
        post_type = request.path.split('/')[-1]
    else:
        post_type = request.path.split('/')[-2]
    queryset = Post.objects.filter(post_type=post_type).order_by('-created_on')
    #reshape posts into side-by-side pairs
    post_pairs = []
    for i in range(0,len(queryset),2):
        try:
            post_pairs.append([queryset[i],queryset[i+1]])
        except:
            post_pairs.append([queryset[i],None])
    template_name = 'building_blocks/post-list.html'
    context = copy.deepcopy(base_context)
    context["post_pairs"] = post_pairs
    context["header_content"] = post_type
    return render(request,template_name,context)

def current_view(request):
    queryset = Post.objects.filter(current=True).order_by('-created_on')
    #reshape posts into side-by-side pairs
    post_pairs = []
    for i in range(0,len(queryset),2):
        try:
            post_pairs.append([queryset[i],queryset[i+1]])
        except:
            post_pairs.append([queryset[i],None])
    template_name = 'building_blocks/post-list.html'
    context = copy.deepcopy(base_context)
    context["post_pairs"] = post_pairs
    context["header_content"] = 'currently'
    return render(request,template_name,context)