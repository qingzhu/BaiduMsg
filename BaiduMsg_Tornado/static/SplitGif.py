#!/usr/bin/env python
#coding: utf8

from PIL import Image
import os

def split_gif(num, filename):
    im = Image.open('pic/'+filename)
    t = Image.new('P',im.size)
    p = im.getpalette()
    os.mkdir(str(num))
    c = 1
    try:
        while True:
            im.seek(im.tell()+1)
            t = im.copy()
            t.putpalette(p)
            t.save('%s/%s.gif' % (num,c))
            c += 1
    except EOFError:
        pass

def main():
    filenames = os.listdir('./pic')
    num = 0
    for filename in filenames:
        if filename.endswith('.gif'):
            num += 1
            split_gif(num,filename)
    print "Total %s gifs." % num


if __name__ == "__main__":
    main()
