from core.models import *
import markdown
import time
from django.template.loader import render_to_string
import re
import json

from .webimage import *

b= open('core/templates/building_blocks/block.html','r')
br=b.readlines()
b.close()
startblock =''.join(br[:2])
endblock = ''.join(br[-2:])


class webPage(object):
    def __init__(self,filepath):
        self.filepath = filepath
        print(self.filepath)
        self.post_type = self.filepath.split('/')[1]
        self.images = []
        self.meta,self.markdown= self._parse_meta()
        self.content=self._parse_content()
    def _parse_meta(self):
        p = open(self.filepath,'r')
        page =p.read()
        p.close()
        yaml = [x.split(':') for x in page.split('---')[1].split('\n')][1:-1]
        markdown = page.split('---')[2]
        meta = {}
        for y in yaml:
            meta[y[0].strip()]=y[1].strip()
        try:
            album_name, img_name = tuple(meta['cover_photo'].strip().split('/'))
            meta['cover_photo'] = Photo.objects.get(filename=img_name,album=Album.objects.get(name=album_name))
            self.images.append(meta['cover_photo'])
        except Exception as e:
            print(e)
            raise Exception('Post must have valid coverphoto specified.')
        try:
            meta['location'] = Location.objects.get(name=meta['location'])
        except Exception as e:
            print(e)
            raise Exception('Post must have valid location specified.')
        if meta['created_on'] == '!today':
            meta['created_on'] = time.strftime('%Y-%m-%d')
        meta['post_type'] = self.filepath.split('/')[1]
        return meta,markdown
    def _parse_content(self):
        data = {}
        md = re.split('__',self.markdown) #sort template keys
        for i in range(1,len(md),4):
            data[md[i]] = md[i+1].strip()
            if md[i+2] != 'END'+md[i]:
                print(md)
                raise Exception('Error: parser could not decode key mappings. \
                                Make sure all content is enclosed between __$KEY$__ and __END$KEY$__ tags.')
        for key in data:
            contents =iter(data[key].split('\n'))
            value = []
            item = next(contents,None)
            if item.startswith('!readjson'):
                data[key] = json.loads(open(os.path.join('static/assets/',item.split(' ')[1].strip())).read())
                print(data[key])
            elif item.startswith('!python'):
                data[key] = eval(item.split(' ')[1].strip())
            else:
                while item is not None:
                    if len(item) == 0:
                        pass
                    elif item.startswith('!block'):
                        value.append(startblock)
                    elif item.startswith('!endblock'):
                        value.append(endblock)
                    elif item.startswith('!pdf'):
                        value.append(render_to_string('building_blocks/pdf.html',{'pdf_file':item.split(' ')[1]}))
                    elif item.startswith('!video'):
                        value.append(render_to_string('building_blocks/video.html',{'video_file':item.split(' ')[1]}))
                    elif item.startswith('!gallery'):
                        album_name = item.split(' ')[1].strip()
                        album = Album.objects.get(name=album_name)
                        photo_list = Photo.objects.filter(album=album)
                        self.images += photo_list
                        value.append(render_to_string('building_blocks/gallery.html',{'photo_list':photo_list}))
                    elif item.startswith('!text+img'):
                        text = ""
                        item = next(contents,'')
                        while not item.startswith('!img'):
                            text += markdown.markdown(item)
                            item = next(contents,'')
                        kwargs = item.strip().split(' ')[1:]
                        print(kwargs)
                        img = webImage(kwargs[0])
                        self.images.append(img.modelinstance)
                        attrs = ['url','title','caption']
                        if '--nocaption' in kwargs:
                            attrs.remove('caption')
                        if '--notitle' in kwargs:
                            attrs.remove('title')
                        value.append(render_to_string('building_blocks/text-img.html',{'text':text,'photo':img.to_dict(attrs)}))
                    elif item.startswith('!figs'):
                        kwargs = item.strip().split(' ')[1:]
                        paths = [i for i in kwargs if not i.startswith('--')]
                        attrs = ['url','title','caption']
                        if '--nocaption' in kwargs:
                            attrs.remove('caption')
                        elif '--notitle' in kwargs:
                            attrs.remove('title')
                        photos = [webImage(p) for p in paths]
                        self.images += [p.modelinstance for p in photos]
                        template_file = f'building_blocks/{len(photos)}img.html'
                        value.append(render_to_string(template_file,{'photo_list':[p.to_dict(attrs) for p in photos]}))
                    elif item.startswith('!button'):
                        text = next(contents,'').strip()
                        link = next(contents,'').strip()
                        value.append(render_to_string('building_blocks/button_centered.html',{'text':text,'link':link}))
                    elif item.startswith('-'):
                        value.append(render_to_string('building_blocks/bullet.html',{'bullet':item[1:]}))
                    else:
                        value.append(markdown.markdown(item))
                    item = next(contents,None)
                data[key] = ''.join(value)
        return data
    def register_as_Post(self):
        instance = Post.objects.create(**self.meta,content=self.filepath)
        instance.save()
        for obj in self.images:
            obj.link = f"https://dahlia.is/{self.post_type}/{self.meta['slug']}"
            obj.save()
        return instance

       
