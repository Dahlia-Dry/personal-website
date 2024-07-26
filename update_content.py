import os
import django
import sys
import gdown

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal-website.settings')
django.setup()

from core.models import *
from utilities.webimage import *
from utilities.webpage import *
from utilities.weblocation import *

def update_locations():
    """
    this function automatically syncs the Location database with the contents of locations.yaml.
    Locations that have been added via admin are also synced back to locations.yaml.
    """
    locdata = yaml_to_dict()
    #first, upload to db from .yaml
    for name in locdata:
        l = webLocation(name=name,**locdata[name])
        l.register_as_Location()
    #next, check for db objects not in .yaml
    locobjs = Location.objects.all()
    for instance in locobjs:
        if instance.name not in locdata:
            try:
                l = webLocation(name=instance.name,address=instance.address,coords=(instance.lat,instance.long))
                l.update_yaml()
            except:
                Location.delete(instance)

def update_imgs():
    """
    this function automatically syncs the Photo and Album databases with the contents of the media folder. 
    """
    img_gen = os.walk('media/')
    next(img_gen) #skip top level
    #first, add new images/albums
    albums = []
    for pathset in img_gen:
        album_name = pathset[0].split('/')[1]
        if album_name == 'temp':
            continue
        albums.append(album_name)
        imgs = [os.path.join(pathset[0],i) for i in pathset[2] if not i.startswith('.')]
        try:
            album = Album.objects.get(name=album_name)
        except:#need to create new Album
            album = Album.objects.create(name=album_name)
            album.save()
        for i in range(len(imgs)):
            img = webImage(imgs[i])
    #then, delete Photos/Albums no longer in media filetree
    album_objs = Album.objects.all()
    photo_objs = Photo.objects.all()
    delete = []
    for p in photo_objs:
        if p.image.url.startswith('/'):
            if not os.path.exists(p.image.url[1:]):
                delete.append(p)
        else:
            if not os.path.exists(p.image.url):
                delete.append(p)
    for a in album_objs:
        if a.name not in albums:
            delete.append(a)
    for obj in delete:
        obj.delete()
    #save all AstroPhotos to make sure gallery links are updated
    for a in AstroPhoto.objects.all():
        a.save()

def update_posts():
    """
    this function syncs the content filetree to the Post database
    """
    content_gen = os.walk('content/')
    next(content_gen) #skip top level
    #first, clear Post database
    posts = Post.objects.all()
    for p in posts:
        p.delete()
    #next, make a new post for every .md file in content subdirectories
    fails = []
    for subdomain in content_gen:
        pages = [os.path.join(subdomain[0],i) for i in subdomain[2] if not i.startswith('.')]
        for p in pages:
            try:
                wp = webPage(p)
                instance = wp.register_as_Post()
                print(f'Post added at http://127.0.0.1:8000/{instance.post_type}/{instance.slug}.')
            except:
                print('failure at ',p)
                #try again if fails (references other post)
                fails.append(p)
    for p in fails:
        wp = webPage(p)
        instance = wp.register_as_Post()
        print(f'Post added at http://127.0.0.1:8000/{instance.post_type}/{instance.slug}.')

def hard_reset():
    os.system('rm db.sqlite3')
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    os.system('python manage.py createsuperuser')

def fetch_media():
    os.system('rm -rf media')
    media_url = "https://drive.google.com/drive/u/0/folders/1K_WCuWkBunv-597s-7FWuwXcqWR8rZR8"
    asset_url = "https://drive.google.com/drive/u/0/folders/1TLK9W-ETWDIz1IaXmCN5VCjFOuCKNaYf"
    print("downloading media...")
    gdown.download_folder(media_url, quiet=True, use_cookies=False)
    print("downloading assets...")
    gdown.download_folder(asset_url, quiet=True, use_cookies=False)
    os.system('rm -rf static/assets')
    os.system('mv assets static/assets')

if __name__ == "__main__":
    if len(sys.argv) >1:
        for arg in sys.argv:
            if arg =='--hard-reset':
                hard_reset()
            elif arg == '--fetch-media':
                fetch_media()
    update_locations()
    update_imgs()
    update_posts()