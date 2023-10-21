from django.db import models
from taggit.managers import TaggableManager
from image_cropping import ImageRatioField
from PIL import Image
import os
import datetime
import uuid

TYPES = ((0,'researching'),
        (1,'on-a-bike'),
        (2,'in-new-places'),
        (3,'lost-in-space'),
        (4,'thinking'),
        (5,'applying'),
        (6,'currently'))

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
    def save(self, *args, **kwargs):
        if not os.path.exists(f'media/{self.name}'):
            os.system(f'mkdir media/{self.name}')
        if self.sync_location:
            photos = Photo.objects.filter(album=self)
            for photo in photos:
                photo.location = self.location
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
    show_on_homepage = models.BooleanField(default=True)
    link = models.CharField(default='https://www.dahlia.is/here',max_length=200,blank=True,null=True)
    def save(self, *args, **kwargs):
        self.filename = self.image.url.split('/')[-1]
        self.image='/'.join(self.image.url.split('/')[-2:])
        if os.path.exists(f'media/temp/{self.filename}'):
            os.system(f'mv media/temp/{self.filename} media/{self.album.name}/{self.filename}')
            self.image=f'{self.album.name}/{self.filename}'
        super(Photo, self).save(*args, **kwargs)
    class Meta:
        ordering = ['album','-created_on']

    def __str__(self):
        return self.title

class AstroPhoto(Photo):
    uid = models.UUIDField(default=uuid.uuid4, editable=False) 
    instruments = models.TextField(blank=True)
    catalog_name = models.TextField(blank=True)
    info_link = models.TextField(blank=True)
    def save(self, *args, **kwargs):
        self.album=Album.objects.get(name='astrophotos')
        self.filename = self.image.url.split('/')[-1]
        self.image='/'.join(self.image.url.split('/')[-2:])
        self.link = f'https://www.dahlia.is/lost-in-space/{self.uid}'
        super(AstroPhoto, self).save(*args, **kwargs)
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True,blank=True,null=True)
    summary = models.TextField(blank=True)
    content=models.FilePathField(path='content/',recursive=True)
    cover_photo = models.ForeignKey(Photo,on_delete=models.CASCADE)
    post_type = models.CharField(max_length=200)
    created_on = models.DateField()
    location = models.ForeignKey(Location, blank=True,null=True,on_delete=models.CASCADE)
    html = models.FilePathField(path='core/templates/',recursive=True,max_length=200,default='core/templates/building_blocks/post-detail.html')
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
