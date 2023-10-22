from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from django.conf import settings

import sys
sys.path.append('..')
from utilities.webpage import *

MENU= json.loads(open(os.path.join(settings.STATIC_ROOT,'assets/here/menu.json')).read())

def redirect_home(request):
    response = redirect('/here')
    return response

def root_view(request):
    context ={}
    if not request.path.endswith('/'):
        post_type = request.path.split('/')[-1]
    else:
        post_type = request.path.split('/')[-2]
    context["post"] = Post.objects.get(slug=post_type)
    post_data = webPage(context['post'].content)
    template_dir = os.path.split(post_data.meta['html'])
    template_name = os.path.join(template_dir[0].split('/')[-1],template_dir[1])
    context["header_content"] = post_data.meta['post_type']
    context["menu"] = MENU
    for key in post_data.content:
        context[key] = post_data.content[key]
    return render(request, template_name, context)

def custom_404(request, exception):
    context={}
    context["header_content"] = 'lost?'
    context["menu"] = MENU
    return render(request, 'pages_html/404.html', context=context,status=404)

def astrophoto_gallery(request):
    queryset = AstroPhoto.objects.all()
    template_name = 'pages_html/lost-in-space.html'
    context = {}
    context['photo_list'] = queryset
    context['header_content'] = 'lost-in-space'
    context['menu'] = MENU
    return render(request,template_name,context)

def detail_view(request,slug):
    if not request.path.endswith('/'):
        slug = request.path.split('/')[-1]
    else:
        slug = request.path.split('/')[-2]
    context ={}
    context["post"] = Post.objects.get(slug=slug)
    post_data = webPage(context['post'].content)
    template_dir = os.path.split(post_data.meta['html'])
    template_name = os.path.join(template_dir[0].split('/')[-1],template_dir[1])
    context["header_content"] = post_data.meta['post_type']
    context["menu"] = MENU
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
    context = {}
    context["post_pairs"] = post_pairs
    context["header_content"] = post_type
    context["menu"] = MENU
    return render(request,template_name,context)

