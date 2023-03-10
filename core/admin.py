from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import *

class Location_admin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class Post_admin(admin.ModelAdmin):
    list_display = ('title', 'slug','created_on')
    list_filter = ("post_type",)
    search_fields = ['title', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    
class Photo_admin(admin.ModelAdmin):
    list_display = ('title','created_on')
    list_filter = ("album",)
    search_fields = ['title', 'caption']

class AstroPhoto_admin(admin.ModelAdmin):
    list_display = ('title','created_on')
    search_fields = ['title', 'caption']

# Register your models here.
admin.site.register(Post,Post_admin)
admin.site.register(Location,Location_admin)
admin.site.register(Photo,Photo_admin)
admin.site.register(AstroPhoto,AstroPhoto_admin)
admin.site.register(Album)