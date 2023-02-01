from django.db import models
from taggit.managers import TaggableManager

TYPES = ((0,'project'),
        (1,'outside'),
        (2,'travel'),
        (3,'astro'),
        (4,'writing'),
        (5,'job'),
        (6,'current project'))
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
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField()
    fulltext=models.TextField()
    type = models.IntegerField(choices=TYPES, default=0)
    cover_photo = models.ImageField(upload_to ='cover_photos/')
    created_on = models.DateField()
    location = models.ManyToManyField(Location)
    use_template = models.BooleanField()
    photo_group=models.ManyToManyField(Album,blank=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
class Photo(models.Model):
    title = models.CharField(max_length=200, unique=True)
    caption = models.TextField()
    image = models.ImageField(upload_to ='images/')
    created_on = models.DateField()
    album = models.ManyToManyField(Album)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
