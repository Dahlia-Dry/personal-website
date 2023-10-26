from core.models import *
import markdown
import time
from django.template.loader import render_to_string
import re
import json
from django.conf import settings

from .webimage import *

print('CWD',os.getcwd())
b= open(os.path.join(settings.BASE_DIR,'core/templates/building_blocks/block.html'),'r')
br=b.readlines()
b.close()
startblock =''.join(br[:2])
endblock = ''.join(br[-2:])


class webPage(object):
    def __init__(self,filepath):
        self.filepath = filepath
        print('processing ',self.filepath)
        self.post_type = self.filepath.split('/')[1]
        self.images = []
        self.registered_html_commands = ['!block','!endblock','!pdf',
                                         '!video','!gallery','!figs',
                                         '!button','!linkbox','!text+img']
        self.meta,self.markdown= self._parse_meta()
        self.content=self._parse_content()
    def _markdown_to_html(self,textblock):
        #slightly modifies markdown.markdown() output
        md = markdown.markdown(textblock)
        md = md.replace('<a ','<a target=_blank ')
        md = md.replace('<ul>','<ul class="u-text u-text-default u-text-2" style="font-size: 0.75rem;"> ')
        
        return md
    def _parse_meta(self):
        p = open(os.path.join(settings.BASE_DIR,self.filepath),'r')
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
            meta['cover_photo'] = None
        try:
            meta['location'] = Location.objects.get(name=meta['location'])
        except Exception as e:
            print(e)
            meta['location']= None
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
            if data[key].startswith('!readjson'):
                item = data[key].strip()
                #parse to dict
                data[key] = json.loads(open(os.path.join(settings.STATIC_ROOT,'assets',item.split(' ')[1].strip())).read())
            elif data[key].startswith('!python'):
                item = data[key].strip()
                #parse to python 
                data[key] = eval(item.split(' ')[1].strip())
            else:
                contents =iter(data[key].split('\n'))
                #parse to html str
                value = []
                item= next(contents,None)
                while item is not None:
                    if item.startswith('!block'):
                        value.append(startblock)
                    elif item.startswith('!endblock'):
                        value.append(endblock)
                    #one line commands
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
                        link= item.split(' ')[1]
                        text = ' '.join(item.split(' ')[2:])
                        value.append(render_to_string('building_blocks/button_centered.html',{'text':text,'link':link}))
                    #text block commands
                    elif item.startswith('!linkbox'):
                        text = []
                        headline = next(contents,'')
                        item = next(contents,'')
                        while not item.startswith('!link'):
                            text.append(item)
                            item = next(contents,'')
                        link = item.strip().split(' ')[1]
                        value.append(render_to_string('building_blocks/linkbox.html',{'text':self._markdown_to_html('\n'.join(text)),
                                                                                      'headline':self._markdown_to_html(headline),
                                                                                      'link':link}))
                    elif item.startswith('!text+img'):
                        text = []
                        item = next(contents,'')
                        while not item.startswith('!img'):
                            text.append(item)
                            item = next(contents,'')
                        kwargs = item.strip().split(' ')[1:]
                        img = webImage(kwargs[0])
                        self.images.append(img.modelinstance)
                        attrs = ['url','title','caption']
                        if '--nocaption' in kwargs:
                            attrs.remove('caption')
                        if '--notitle' in kwargs:
                            attrs.remove('title')
                        value.append(render_to_string('building_blocks/text-img.html',{'text':self._markdown_to_html('\n'.join(text)),
                                                                                       'photo':img.to_dict(attrs)}))
                    else:
                        text = []
                        while item is not None and not any([item.startswith(c) for c in self.registered_html_commands]):
                            text.append(item)
                            item = next(contents,None)
                        value.append(self._markdown_to_html('\n'.join(text)))
                        continue
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

       
