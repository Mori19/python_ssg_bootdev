#!/usr/bin/env python

import shutil
import os

from operations import generate_page_recursive
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def copy_to_public(src,dst,path):
    here = os.listdir(f'{src}{path}')
    def inner(a):
        if os.path.isdir(f'{src}{path}{a}'):
            print(f'make {dst}{path}{a}')
            os.mkdir(f'{dst}{path}{a}')
            copy_to_public(src,dst,f'{path}{a}/')
        else:
            print(f"copy {src}{path}{a}/ to {dst}{path}{a}/")
            shutil.copy(f'{src}{path}{a}', f'{dst}{path}{a}')
    list(map(inner,here))

if __name__ == '__main__':
    shutil.rmtree('/home/mori/Documents/dev/bootdev/static_site_generator/public/')
    os.mkdir('public')
    copy_to_public('./static','./public','/')
    generate_page_recursive('content','template.html','public')


