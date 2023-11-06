from PIL import Image
import datetime
from core.models import *

class webImage(object):
    """this class converts a filepath within the media/ directory into a Photo object in django db"""
    def __init__(self,filepath):
        self.filepath = filepath
        self.filename = self.filepath.split('/')[-1]
        self.album_name = self.filepath.split('/')[-2]
        try:
            self.album = Album.objects.get(name=self.album_name)
        except:
            raise Exception(f'{self.album_name} does not exist.')
        self.modelinstance = self.register_as_Photo()
    def get_date_taken(self):
        try:
            exif = Image.open(self.filepath)._getexif()
            date = exif[36867]
            return date.split(' ')[0].replace(':','-')
        except:
            date=datetime.datetime.today().strftime('%Y-%m-%d')
            return date
    def register_as_Photo(self):
        try:
            if self.album_name == 'astrophotos':
                instance = AstroPhoto.objects.get(filename=self.filename)
            else:
                instance = Photo.objects.get(album=self.album,filename=self.filename)
        except Exception as e:
            #print(e)
            if self.album_name == 'astrophotos':
                instance =AstroPhoto.objects.create(title=self.filename.split('.')[0],
                                            image=self.filepath,
                                            location = self.album.location,
                                            album=self.album,
                                            created_on=self.get_date_taken())
                instance.save()
                print(f'created new AstroPhoto {instance.title}')
            else:
                try: #check if album name changed, ask user
                    instance=Photo.objects.get(filename=self.filename)
                    print(len(instance.album_name),len(self.album_name))
                    c= input(f'Instance of {instance.filename} found registered under album {instance.album.name}. \
                        Change album name {instance.album.name} to {self.album_name}? y/n: ')
                    if c=='y':
                        old_album = instance.album
                        instance.album = self.album
                        self.album.location = old_album.location
                        self.album.save()
                        changephotos = Photo.objects.filter(album=old_album)
                        for photo in changephotos:
                            photo.album=self.album
                except:#no instance found; create one
                    instance =Photo.objects.create(title=self.filename.split('.')[0],
                                            image=self.filepath,
                                            location = self.album.location,
                                            album=self.album,
                                            created_on=self.get_date_taken())
                    instance.save()
                    print(f'created new Photo {instance.title}')
        return instance
    def to_dict(self,attrs=['url','title','caption']):
        d = {}
        for a in attrs:
            if a =='url':
                d[a] = self.modelinstance.image.url
            else:
                d[a] = getattr(self.modelinstance,a,None)
        return d