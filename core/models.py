from django.db import models
from taggit.managers import TaggableManager
from image_cropping import ImageRatioField

TYPES = ((0,'busy'),
        (1,'outside'),
        (2,'in-new-places'),
        (3,'lost-in-space'),
        (4,'thinking'),
        (5,'at-work'),
        (6,'currently'))
class Location(models.Model):
    name=models.CharField(max_length=200, unique=True)
    lat =models.FloatField()
    long=models.FloatField()
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Album(models.Model):
    name = models.CharField(max_length=200,unique=True)
    type = models.IntegerField(choices=TYPES, default=0)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField(blank=True)
    fulltext=models.TextField(blank=True)
    post_type = models.IntegerField(choices=TYPES, default=0)
    cover_photo = models.ImageField(upload_to ='cover_photos/')
    created_on = models.DateField()
    location = models.ManyToManyField(Location)
    html_file = models.CharField(max_length=200,default='building_blocks/base.html')
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Photo(models.Model):
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to ='images/')
    location = models.ForeignKey(Location, blank=True,on_delete=models.CASCADE)
    created_on = models.DateField()
    album = models.ManyToManyField(Album)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class AstroPhoto(Photo):
    instruments = models.TextField(blank=True)
    catalog_name = models.TextField(blank=True)
    link = models.TextField(blank=True)
    

