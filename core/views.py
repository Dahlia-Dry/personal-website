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
    queryset = Photo.objects.filter(album__name='astrophotos').order_by('-created_on')
    template_name = 'pages/lost-in-space.html'
    def get_context_data(self,**kwargs):
        context = super(astrophoto_list,self).get_context_data(**kwargs)
        context['header_content'] = 'lost-in-space'
        return context
        
class current_project_list(generic.ListView):
    queryset = Post.objects.filter(post_type=6).order_by('-created_on')
    template_name = 'building_blocks/post-list.html'
    def get_context_data(self,**kwargs):
        context = super(current_project_list,self).get_context_data(**kwargs)
        context['header_content'] = 'currently'
        return context

def rle(request):
    return render(request,'pages/rle.html',{'header_content':'currently'})

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

