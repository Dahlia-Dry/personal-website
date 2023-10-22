from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import *
import os

class Location_admin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class Instrument_admin(admin.ModelAdmin):
    list_display = ['name','name_short']
    search_fields = ['name','name_short']

class Post_admin(admin.ModelAdmin):
    list_display = ('title', 'slug','created_on')
    list_filter = ("post_type",)
    search_fields = ['title', 'summary']
    prepopulated_fields = {'slug': ('title',)}

class Photo_admin(admin.ModelAdmin):
    list_display = ('title','created_on','album')
    list_filter = ("album",)
    search_fields = ['title', 'caption']
    exclude=('filename',)

class Album_admin(admin.ModelAdmin):
    pass
        

class AstroPhoto_admin(admin.ModelAdmin):
     list_display = ('title','created_on')
     search_fields = ['title', 'caption']
     exclude=('filename',)

# Register your models here.
admin.site.register(Post,Post_admin)
admin.site.register(Location,Location_admin)
admin.site.register(Instrument,Instrument_admin)
admin.site.register(Photo,Photo_admin)
admin.site.register(AstroPhoto,AstroPhoto_admin)
admin.site.register(Album,Album_admin)