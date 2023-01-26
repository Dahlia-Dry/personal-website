from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import *

class photo_list(generic.ListView):
    queryset = astro_photo.objects.filter(status=1).order_by('-created_on')
    template_name = 'lost-in-space.html'
    def get_context_data(self,**kwargs):
        context = super(photo_list,self).get_context_data(**kwargs)
        context['header_content'] = 'dahlia.is/lost-in-space'
        return context

# class PostDetail(generic.DetailView):
#     model = astro_photo
#     template_name = 'post_detail.html'


# Create your views here.
def space(request):
    return render(request,'space-diff.html',{'header_content':'dahlia.is/lost-in-space'})

