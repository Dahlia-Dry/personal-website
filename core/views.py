from django.shortcuts import render,redirect
from django.http import HttpResponse

def home(request):
    return render(request,'here.html')

def currently(request):
    return render(request,'base.html',{'header_name':'dahlia.is/currently'})

def zoomin(request):
    return render(request,'base.html',{'header_name':'dahlia.is/zoomin'})

def places(request):
    return render(request,'base.html',{'header_name':'dahlia.is/in-new-places'})

def thinking(request):
    return render(request,'base.html',{'header_name':'dahlia.is/thinking'})

def learning(request):
    return render(request,'base.html',{'header_name':'dahlia.is/learning'})

def space(request):
    return render(request,'base.html',{'header_name':'dahlia.is/lost-in-space'})

def outside(request):
    return render(request,'base.html',{'header_name':'dahlia.is/outside'})

def busy(request):
    return render(request,'base.html',{'header_name':'dahlia.is/busy'})

def job(request):
    return render(request,'base.html',{'header_name':'dahlia.is/looking-for-a-job'})

def redirect_home(request):
    response = redirect('/here')
    return response