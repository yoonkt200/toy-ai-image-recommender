from PIL import Image
import os

def is_jpg(filename):
    try:
        i=Image.open(filename)
        return i.format =='JPEG'
    except IOError:
        return False


rootdir = '/Users/yoon/Desktop/clothes/'
arr = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filee = os.path.join(subdir, file)
        if is_jpg(filee) == False:
            arr.append(filee)

for i in arr:
    print (i)