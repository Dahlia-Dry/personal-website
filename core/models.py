from django.db import models
from taggit.managers import TaggableManager
from image_cropping import ImageRatioField
from PIL import Image
import os
import datetime
import uuid

def get_date_taken(path):
    exif = Image.open(path)._getexif()
    if not exif:
        return datetime.datetime.now().date()
    d = exif[36867]
    return datetime.date(year=int(d.split(':')[0]),month=int(d.split(':')[1]),day=int(d.split(':')[2]))
class Location(models.Model):
    name=models.CharField(max_length=200, unique=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    lat =models.FloatField(blank=True,null=True)
    long=models.FloatField(blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
class Album(models.Model):
    name = models.CharField(max_length=200,unique=True)
    location = models.ForeignKey(Location, blank=True,null=True,on_delete=models.CASCADE)
    sync_location = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    link = models.CharField(default='https://www.dahlia.is/here',max_length=200,blank=True,null=True)
    def save(self, *args, **kwargs):
        if not os.path.exists(f'media/{self.name}'):
            os.system(f'mkdir media/{self.name}')
        photos = Photo.objects.filter(album=self)
        for photo in photos:
            if self.sync_location:
                photo.location = self.location
            photo.show_on_homepage = self.show_on_homepage
            photo.save()
        super(Album, self).save(*args, **kwargs)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
class Photo(models.Model):
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to ='temp/')
    location = models.ForeignKey(Location, blank=True,null=True,on_delete=models.CASCADE)
    created_on = models.DateField()
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    filename = models.CharField(max_length=200,blank=True,null=True)
    show_on_homepage = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        self.filename = self.image.url.split('/')[-1]
        self.image='/'.join(self.image.url.split('/')[-2:])
        self.show_on_homepage = self.album.show_on_homepage
        if os.path.exists(f'media/temp/{self.filename}'):
            os.system(f'mv media/temp/{self.filename} media/{self.album.name}/{self.filename}')
            self.image=f'{self.album.name}/{self.filename}'
        super(Photo, self).save(*args, **kwargs)
    class Meta:
        ordering = ['album','-created_on']

    def __str__(self):
        return self.title
    
class Instrument(models.Model):
    name = models.CharField(max_length=200)
    name_short = models.CharField(max_length=200,blank=True,null=True)
    link=models.CharField(max_length=200,blank=True,null=True)

class AstroPhoto(Photo):
    instruments = models.ManyToManyField(Instrument,blank=True)
    catalog_name = models.TextField(blank=True)
    info_link = models.TextField(blank=True)
    inst_caption = models.TextField(default='',blank=True,null=True)
    def instruments_to_str(self):
        inst_str = []
        for inst in self.instruments.all():
            if inst.link is not None:
                inst_str.append(f"""<a href="{inst.link}" target="_blank">{inst.name_short}</a>""")
            else:
                inst_str.append(f"{inst.name_short}")
        return ','.join(inst_str)
    def save(self, *args, **kwargs):
        self.album=Album.objects.get(name='astrophotos')
        self.filename = self.image.url.split('/')[-1] 
        try:
            self.inst_caption = 'Imaged with '+ self.instruments_to_str()+ '.'
        except:
            self.inst_caption = ""
        #print(self.inst_caption)
        self.image='/'.join(self.image.url.split('/')[-2:])
        super(AstroPhoto, self).save(*args, **kwargs)
        
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True,blank=True,null=True)
    content=models.FilePathField(path='content/',recursive=True)
    cover_photo = models.ForeignKey(Photo,on_delete=models.CASCADE,blank=True,null=True)
    post_type = models.CharField(max_length=200)
    created_on = models.DateField()
    current=models.BooleanField(default=False)
    location = models.ForeignKey(Location, blank=True,null=True,on_delete=models.CASCADE)
    html = models.FilePathField(path='core/templates/',recursive=True,max_length=200,default='core/templates/building_blocks/post-detail.html')
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
