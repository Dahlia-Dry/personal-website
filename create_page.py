import os
import sys

def create_page(path):
    md_template = open('core/templates/pages_markdown/base.md').read()
    print(os.path.join('content/',path))
    f=open(os.path.join('content/',path),'w')
    f.write(md_template)
    f.close()

if __name__ == "__main__":
    if len(sys.argv) >1:
        try:
            path = sys.argv[1]
            create_page(path.strip())
        except:
            raise Exception('Error creating markdown template: must specify filepath as [post_type]/[post_name].md')
    else:
        raise Exception('Error creating markdown template: must specify filepath as [post_type]/[post_name].md')