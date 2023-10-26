---
title: homepage
slug: here
cover_photo: here/profile.JPG
created_on: !today
location: MIT
html: pages_html/here.html
tags:
---
__BIO__
!block
# Hi! My name is Dahlia.
### Welcome to my little corner of the internet :)
!endblock
!text+img
I'm a [recent MIT grad](https://impactclimate.mit.edu/2023/09/27/student-spotlight-mcsc-scholar-dahlia-dry/) with a B.S. in physics and electrical engineering. Currently, I'm living in Copenhagen and working at a startup called [TEGnology](https://www.tegnology.dk). Things I love include my aggressively blue foldy bike, running in the rain, spending long nights at telescopes, and collecting cozy sweaters. I'm passionate about working at the interface between software and hardware to build the data infrastructures that will be the backbone of a sustainable future. My plan is to go wherever that takes me, and make sure to have plenty of fun along the way.
!img here/profile.JPG --nocaption --notitle
__ENDBIO__
__GALLERY__
!python Photo.objects.order_by('?').filter(show_on_homepage=True)
__ENDGALLERY__
__TILES__
!readjson here/tiles.json
__ENDTILES__