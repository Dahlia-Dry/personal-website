from PIL import Image
import os

def compress_folder(folder):
    imgs = os.listdir(f'media/{folder}')
    for img in imgs:
        if not img.startswith('.') and not img.endswith('.gif'):
            p = os.path.join(f'media/{folder}',img)
            print(f'compressing {p}')
            foo = Image.open(p)
            foo.save(p, optimize=True, quality=85) 

compress_folder('roskilde-fjord')
compress_folder('seattle')