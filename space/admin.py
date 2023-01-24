from django.contrib import admin
from .models import *

# Register your models here.
class Astro_admin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'caption']
    prepopulated_fields = {'slug': ('title',)}
# Register your models here.
admin.site.register(astro_photo,Astro_admin)