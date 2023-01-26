from django.db import models

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class astro_photo(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    caption = models.TextField()
    photo = models.ImageField(upload_to ='space/')
    created_on = models.DateField()
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

