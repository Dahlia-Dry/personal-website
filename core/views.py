from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import generic
from .models import *

def home(request):
    return render(request,'here.html')

def redirect_home(request):
    response = redirect('/here')
    return response
class astrophoto_list(generic.ListView):
    queryset = Photo.objects.filter(album__name='astrophotos').order_by('-created_on')
    template_name = 'lost-in-space.html'
    def get_context_data(self,**kwargs):
        context = super(astrophoto_list,self).get_context_data(**kwargs)
        context['header_content'] = 'dahlia.is/lost-in-space'
        return context

def rle(request):
    return render(request,'rle.html',{'header_content':'dahlia.is/here'})

def currently(request):
    return render(request,'base.html',{'header_content':'dahlia.is/currently'})

def notes(request):
    return render(request,'base.html',{'header_content':'dahlia.is/taking-notes'})

def places(request):
    return render(request,'base.html',{'header_content':'dahlia.is/in-new-places'})

def thinking(request):
    return render(request,'base.html',{'header_content':'dahlia.is/thinking'})

def outside(request):
    return render(request,'base.html',{'header_content':'dahlia.is/outside'})

def busy(request):
    return render(request,'base.html',{'header_content':'dahlia.is/busy'})

def job(request):
    return render(request,'base.html',{'header_content':'dahlia.is/employable'})

