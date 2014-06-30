#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from PIL import Image

def binary(f):
    print f
    img = Image.open(f)
    #img = img.convert('1')
    img = img.convert('RGBA')
    
    pixdata = img.load()
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x,y][0] < 90:
                pixdata[x,y] = (0,0,0,255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x,y][1] < 136:
                pixdata[x,y] = (0,0,0,255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x,y][2] > 0:
                pixdata[x,y] = (255,255,255,255)

    return img

num = 0
def division(img):
    """
    分割图像，就是把验证码按字符分割出来
    """
    global num
    font = []
    for i in range(4):
        x = 16+i*15
        y = 2
        temp = img.crop((x,y, x+7, y+10))
        temp.save('./temp/%s.gif' % num)
        num += 1
        font.append(temp)
    return font

def recognize(img):
    fontMods = []
    for i in range(10):
        fontMods.append((str(i), Image.open("./num/%s.gif" % i)))
    result = ""
    font = division(img)
    for i in font:
        target = i
        points = []
        for mod in fontMods:
            diffs = 0
            for yi in range(10):
                for xi in range(7):
                    #print "mod[1].getpixel((xi,yi)):"+str(mod[1].getpixel((xi,yi)))
                    #print "target.getpixel((xi,yi)):"+str(target.getpixel((xi,yi)))
                    if 0 in target.getpixel((xi,yi)):
                        compare = 0
                    else:
                        compare = 255
                    if mod[1].getpixel((xi,yi)) != compare:
                        diffs += 1
            print "diffs:%s" % diffs
            points.append((diffs, mod[0]))
        points.sort()
        result += points[0][1]
    return result

if __name__ == "__main__":
    codedir = './pic/'
    for imgfile in os.listdir(codedir):
        if imgfile.endswith(".gif"):
            mydir = './result/'
            img = binary(codedir+imgfile)
            num = recognize(img)
            mydir += (num+".gif")
            print "save to:%s" % mydir
            img.save(mydir)

