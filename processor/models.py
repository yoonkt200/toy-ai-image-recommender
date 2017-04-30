from django.db import models

import datetime
from django.db.models import Q
from uuid import uuid4
from django.utils.deconstruct import deconstructible
import os

from io import BytesIO
from io import StringIO
from PIL import Image as pil
from django.core.files.uploadedfile import InMemoryUploadedFile


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def imgToThumbnail(img, force=True):
    max_width = 217
    max_height = 217
    input_img = BytesIO(img.read())
    new_img = pil.open(input_img)

    if not force:
        new_img.thumbnail((max_width, max_height), pil.ANTIALIAS)
    else:
        src_width, src_height = new_img.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = max_width, max_height
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = int(src_width - crop_width) // 2
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = int(src_height - crop_height) // 3
        new_img = new_img.crop((x_offset, y_offset, x_offset + int(crop_width), y_offset + int(crop_height)))
        new_img = new_img.resize((dst_width, dst_height), pil.ANTIALIAS)

    tempfile_io = BytesIO()
    new_img.convert('RGB').save(tempfile_io, format='JPEG')
    image_file = InMemoryUploadedFile(tempfile_io, None, 'thumbnail.jpg', 'image/jpeg', 1024, None)

    return image_file


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        now = datetime.datetime.now()
        name = filename.split('.')[0]
        ext = filename.split('.')[-1]

        filepath = self.path + now.strftime("/%Y/%m/%d/%H/%M")
        return os.path.join(filepath, filename)

pF_path_and_rename = PathAndRename("projects")
pI_path_and_rename = PathAndRename("media")


#프로젝트 정보를 담고있는 클래스
class Image(TimeStampedModel):
    title = models.CharField(max_length=200)
    imageFile = models.ImageField(blank=True, null=True, upload_to=pI_path_and_rename, default=None,
                                  height_field="height_field", width_field="width_field")
    thumbnailImg = models.ImageField(blank=True, null=True, upload_to=pF_path_and_rename, default=None,
                                  height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(null=True, default=0)
    width_field = models.IntegerField(null=True, default=0)
    descriptor = models.ManyToManyField('processor.Descriptor')

    def __str__(self):
        return self.title

    @staticmethod
    def createImage(title, image):
        thumbnailImg = imgToThumbnail(image, force=True)
        newImage = Image.objects.create(title=title, imageFile=image, thumbnailImg=thumbnailImg)
        # # Descriptor 분석해서 오브젝트 생성하는 코드 삽입
        newImage.save()
        return newImage


class Descriptor(models.Model):
    tag = models.CharField(max_length=200)
    keyPoint_1 = models.IntegerField(default=0)
    keyPoint_2 = models.IntegerField(default=0)

    def __str__(self):
        return self.tag