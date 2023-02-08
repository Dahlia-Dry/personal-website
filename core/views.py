from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import generic
from .models import *

def home(request):
    return render(request,'pages/here.html',{'header_content':'here'})

def redirect_home(request):
    response = redirect('/here')
    return response

class astrophoto_list(generic.ListView):
    queryset = AstroPhoto.objects.all()
    template_name = 'pages/lost-in-space.html'
    def get_context_data(self,**kwargs):
        context = super(astrophoto_list,self).get_context_data(**kwargs)
        context['header_content'] = 'lost-in-space'
        return context

def create_detail_view(type):
    def detail_view(request,slug):
        # dictionary for initial data with
        # field names as keys
        context ={}
        context["post"] = Post.objects.get(slug=slug)
        template_name = context["post"].html_file
        context["header_content"] = TYPES[type][1]
        return render(request, template_name, context)
    return detail_view

def create_list_view(type_list,title_type=None):
    if title_type is None:
        title_type = type_list[0]
    class list_view(generic.ListView):
        queryset = Post.objects.filter(post_type__in=type_list).order_by('-created_on')
        print('LEN',len(queryset))
        template_name = 'building_blocks/post-list.html'
        def get_context_data(self,**kwargs):
            context = super(list_view,self).get_context_data(**kwargs)
            context['header_content'] = TYPES[title_type][1]
            context['subdir'] = TYPES[title_type][1]+'/'
            return context
    return list_view


def notes(request):
    return render(request,'building_blocks/base.html',{'header_content':'taking-notes'})

def places(request):
    return render(request,'building_blocks/base.html',{'header_content':'in-new-places'})

def thinking(request):
    return render(request,'building_blocks/base.html',{'header_content':'thinking'})

def outside(request):
    return render(request,'building_blocks/base.html',{'header_content':'outside'})

def busy(request):
    return render(request,'building_blocks/base.html',{'header_content':'busy'})

def job(request):
    return render(request,'pages/resume.html',{'header_content':'at-work'})

