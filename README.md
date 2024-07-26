# Welcome to my little corner of the internet! 
I've long wanted a place to document my crafts and adventures that felt like it was mostly just for me but occasionally also to share with others, and figuring out exactly how I wanted to do that with this website has become quite a fun side project for the past year or so. 

It's built using the django python framework and hosted using pythonanywhere. Using some extra scripts and my own flavor of markdown, I've developed a workflow that makes it easy to write and edit full multimedia posts directly in my development environment without fussing with all the html beneath. I'm by all means a webdev amateur so it's definitely not the cleanest or the most efficient, but I'm quite happy with the system I've developed for pretty quickly and seamlessly publishing custom, stylized markdown notes to the web. 
## Design principles
### modularity
- Fuss with css/html formatting as little as possible. Render content dynamically whenever possible. Make template components that are responsive, adaptable, and reusable in a variety of contexts.
- Number of data types and locations should be limited as much as possible
- Subdirectory organization should be clear and consistent
### customizability
- hardcode attributes and metadata as little as possible; leave room for change. 
- Create page templates that can be added to and adjusted with ease; avoid redundant parts arising from minor changes
### simplicity
- arises from the above two implemented well. 
- database-content syncing is automatic and as foolproof as possible; it should be easy to completely wipe the django database in case of a bad migration and recreate everything automatically using local content. 
- Content creation using Markdown; use python to keep the editing interface very high-level, intuitive, and efficient.
##  Database structure
### models.py
Currently, there are 4 main data structures (Django models):
- Post
- Photo
- Album (corresponds to parent directory of Photo)
- Location
Additionally, the AstroPhoto model inherits Photo but adds some other relevant metadata.
### webpage.py
This file defines a python class **webPage** which takes as input the markdown filepath (root directory **content/**) containing the page metadata and content and converts it into a Post object in the django database. The parent directory of the markdown file defines the post type.
#### Template .md file: content/testing/test.md
```
---

title:

slug: test

summary:

cover_photo:

created_on: !today

location:

html: building_blocks/post-detail.html

tags:

---

__CONTENT__

[...]

__ENDCONTENT__
```
#### metadata parsing
The Post object metadata are parsed by the ```self._parse_metadata()``` method of ```WebPage``` 
#### content parsing
The Post object metadata are parsed by the ```self._parse_content()``` method of ```WebPage```. This method returns a context dictionary that can be fed straight to a django template. The default key name is ```CONTENT``` , which maps to a list of html components rendered to strings using ```django.template.loader.render_to_string(template_name,contextdict)```and then included in raw form in post-detail.html.  The html file to render using the returned context dictionary is specified as the ```html``` metadata variable. For  pages where custom components/formatting is desired (e.g. the homepage), additional keys can be specified using the same ```__KEY__``` [...] ```__ENDKEY__``` syntax demonstrated in the template file. 

Within each key, content can be added as plain markdown which will then be converted automatically to html. Additionally, more complex html components such as image galleries, buttons, and videos can be added using a set of defined commands that signal the interpreter to render html from a variety of html template files in **core.templates/building_blocks/**.
##### commands for rendering html blocks
By default, markdown content within the CONTENT key will be rendered as a single html string using the commands below, which is then passed to the default page template using the django variable framework.
###### block/endblock
used to enclose text not otherwise enclosed in a section.
```
!block
# heading
text
[...markdown...]
!endblock
```
###### gallery
```
!gallery [album_name]
```
###### figures
```
!figs album/img1.png album/img2.jpg album2/img3.jpeg [--flag]
```
number of figs can be 1-4
can be used with no flag or a combination of:
```
--nocaption 
--notitle
```
###### text+image
```
!text+img
#heading
text
[...markdown...]
!img album/img.png [--flag]
```
can be used with no flag or a combination of:
```
--nocaption 
--notitle
```
###### button
```
!button
[button text]
[button link]
```
###### pdf
```
!pdf folder/asset.pdf
```
###### video
```
!video folder/asset.mp4
```
###### linkbox
```
!linkbox
headline
text
[...more text..]
!link www.external-link.com
```
##### commands for passing data to templates
###### python variables
e.g. the following lines in the .md file : 
```
__PYTHONVAR__
!python model.objects.filter(key=value)
__ENDPYTHONVAR__
```
will result in a context dict with the 'PYTHONVAR' key set to the result of the query model.objects.filter(key=value). 
###### json data
e.g. the following lines in the .md file:
```
__JSONKEY__
!readjson folder/asset.json
__ENDKEY__
```
will result in a context dict with the 'JSONKEY' dict set to the result of reading the specified json file (relative to root static/assets) using json.loads(). 
### webimage.py
This file defines a python class **webImage** which takes as input the image filepath (root directory **media/**), and then either retrieves or creates the corresponding Photo object in the django database. The parent directory of the image file defines the album name. 
### weblocation.py
This file defines a python class **webLocation** which takes as input the name of a location and either its address or (lat,long) coordinates. Using geopy, the Location object in the django database is either retrieved or created and the local data file **locations.yaml** is updated accordingly.
### update_content.py
This file uses the above 3 classes to sync local content with the django database. The django database follows the local content: changes/deletions to content on the local level should automatically be propagated to the database.
## Graphic design
### Nicepage
I'm much more interested in the python side of development than in getting into the nitty gritty of css formatting, so I decided to use a free webpage creation GUI called Nicepage that allows you to view and copy the raw source code of graphically generated webpages. I realized it would be really cumbersome and inefficient to individually create each page on the site with this tool and copy the html/css/javascript and image files to the appropriate directories, so I instead used this tool to create one single template page with all the graphical components I would want to use in different contexts (image galleries, text blocks, embedded videos, etc). I then export the html and css for this template page and clip it into different component template files found in **core/templates/building_blocks/**. Dynamic rendering of these component files is done in the ```self._parse_content()``` function of ```utilities/webpage.py```.
## Django content creation made simple using Markdown
### views.py
post type inferred from filepath of Post content file.
#### root_view()
dynamically renders all Post objects whose slug is the same as the post type (e.g. dahlia.is/here, dahlia.is/in-the-news, dahlia.is/lost-in-space)
#### list_view()
renders all Post objects of a given post type in list form with links to the Post content page.
#### detail_view()
dynamically renders all Post objects which are part of a post group (e.g. researching/, making/)
### urls.py
- home_urls: home page is dahlia.is/here, dahlia.is/ redirects to dahlia.is/here
- root_urls: correspond to root_view
- list_urls: correspond to list_view
- detail_urls: correspond to detail_view
### static file management
#### content/
All markdown files corresponding to Post objects. The parent directory defines the post type.
#### media/
All image files corresponding to Photo objects. The parent directory defines the album name and corresponding Album object.
#### core/static
all contents of core/static are synced to static/ using ```python manage.py collectstatic```.
##### core/static/assets/
This is where any static content goes that is not registered to the Photo database. Videos, pdfs, etc. Directory structure is single-level (non-recursive). Static files included in ```.md``` content files are specified relative to this root directory.
##### core/static/css
- **building_blocks/** contains core css that is imported into most template files (e.g. ```nicepage.css```, ```page_template.css```)
- **pages/** contains custom additional css for specific pages
##### core/static/js
Javascript files for custom page behavior.
## Example Workflow
### 1. Create new markdown page file
```$ python create_page.py [post_type]/[page-name].md```
Running this command creates a markdown file in the post_type/ subdirectory of content/ with the default yaml header and CONTENT key specified in the example above. Page content can then be created using a combination of markdown and the command list specified [[Website!#content parsing#List of Commands|above]].
### 2. Add media and static files
- Images added via commands to the markdown page file must be located in a subdirectory of media/ corresponding to their album name (e.g. an image located at media/here/profile.JPG can be specified as the cover photo of a post using ```cover_photo : here/profile.JPG```)
- All other assets (videos, pdfs, etc) must be located in a subdirectory of core/static/assets/ and specified relative to this location (e.g. a video located at core/static/assets/here/demo.mp4 can be included in markdown using the command ```!video here/demo.mp4```). Make sure to add assets to core/static/assets and not static/assets because the ```python manage.py collectstatic```sync only works one way.
### 3. Sync django databases to newly added local content
```$ python update_content.py```
### 4. Sync static files to static path
```$ python manage.py collectstatic```
### 5. Check results on development server
```$ python manage.py runserver```
### 6. Set DEBUG=FALSE in settings.py, then push to production