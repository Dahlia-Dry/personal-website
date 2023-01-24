from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import generic

def home(request):
    return render(request,'here.html')

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

def redirect_home(request):
    response = redirect('/here')
    return response