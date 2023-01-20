from django.shortcuts import render,redirect
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. This is Dahlia's corner of the internet.")

def redirect_home(request):
    response = redirect('/here')
    return response