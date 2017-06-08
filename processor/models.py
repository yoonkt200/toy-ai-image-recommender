# -*- coding: utf-8 -*-

from django.db import models

import datetime
import json
from django.db.models import Q
from uuid import uuid4
from django.utils.deconstruct import deconstructible
import os
import csv

import cv2
from skimage.feature import hog
from skimage import data, color, exposure
import numpy as np
import tensorflow as tf

from io import BytesIO
from io import StringIO
from PIL import Image as pil
from django.core.files.uploadedfile import InMemoryUploadedFile


modelFullPath = '/tmp/output_graph.pb'
labelsFullPath = '/tmp/output_labels.txt'

CSV_PATH = "/Users/yoon/Documents/hog_descriptor.csv"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/static/uploads"


def create_graph():
    """저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
    # 저장된(saved) graph_def.pb로부터 graph를 생성한다.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(imagePath):
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # 저장된(saved) GraphDef 파일로부터 graph를 생성한다.
    create_graph()

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
        top_k = predictions.argsort()[-5:][::-1]
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        answer = []
        for i in range(0, 5):
            rank = labels[top_k[i]][1:]
            rank = rank.replace("'", "")
            rank = rank.replace("'", "")
            rank = rank.replace("n", "")
            rank = rank.replace("\\", "")
            answer.append(rank)

        return answer


def strProcessing(hog_str):
    hog_str = hog_str.replace("[", "")
    hog_str = hog_str.replace("]", "")
    hog_str = hog_str.split(',')
    hog_str = np.float32(hog_str)
    return hog_str


def readCSV_HOGinfo():
    f = open(CSV_PATH, 'r')
    csvReader = csv.reader(f, delimiter=',')

    matrix = []

    for temp_row in csvReader:
        matrix.append(np.array(temp_row))

    f.close()

    return matrix


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

pF_path_and_rename = PathAndRename("media")
pI_path_and_rename = PathAndRename("media")


def getFirstKey(item):
    return item[0]


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 이미지 정보를 담고있는 모델
class Image(TimeStampedModel):
    title = models.CharField(max_length=200)
    label = models.CharField(max_length=200, default="", blank=True, null=True)
    imageFile = models.ImageField(blank=True, null=True, upload_to=pI_path_and_rename, default=None,
                                  height_field="height_field", width_field="width_field")
    thumbnailImg = models.ImageField(blank=True, null=True, upload_to=pF_path_and_rename, default=None,
                                  height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(null=True, default=0)
    width_field = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.title

    @staticmethod
    def createImage(title, image):
        thumbnailImg = imgToThumbnail(image, force=True)
        newImage = Image.objects.create(title=title, imageFile=image, thumbnailImg=thumbnailImg)
        newImage.save()
        return newImage

    # 유사한 컬러 히스토그램을 가진 이미지를 랭크를 매기는 함수
    @staticmethod
    def getSimilarColorHistogramImage(obj_idList, latestImage):
        input_image = pil.open(latestImage.imageFile)
        input_image = np.asarray(input_image)

        input_hist = cv2.calcHist([input_image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        input_hist = cv2.normalize(input_hist, input_hist)

        images = Image.objects.filter(pk__in=obj_idList, label=latestImage.label).exclude(id=latestImage.id)
        result_list = []

        for index, img in enumerate(images):
            itImg = pil.open(img.imageFile)
            itImg = np.asarray(itImg)

            hist = cv2.calcHist([itImg], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist, hist)

            compHist = cv2.compareHist(hist, input_hist, 2)
            result_list.append([compHist, img.id])

        result_list = sorted(result_list, key=getFirstKey, reverse=True)
        obj_idList = []
        for index, result in enumerate(result_list):
            obj_idList.append(result[1])

        objs = Image.objects.filter(pk__in=obj_idList)
        qs_sorted = list()
        for id in obj_idList:
            qs_sorted.append(objs.get(id=id))

        return qs_sorted

    # csv 파일의 HOG descriptor 들과 input 이미지의 descriptor 를 비교하여 랭크를 매기는 함수
    @staticmethod
    def compareHOGinfo(input_image):
        matrix = readCSV_HOGinfo()
        input_hog = Image.createHOGinfo(input_image.imageFile)
        result_list = []

        for i in range(0, len(matrix)):
            matrix_hog = matrix[i][0]
            matrix_hog = strProcessing(matrix_hog)
            id = matrix[i][1]

            hog_result = [cv2.compareHist(input_hog, matrix_hog, 0), id]
            result_list.append(hog_result)

        result_list = sorted(result_list, key=getFirstKey, reverse=True)
        obj_idList = []
        for index, result in enumerate(result_list):
            obj_idList.append(result[1])

        if obj_idList:
            with open(CSV_PATH, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([input_hog.tolist(), input_image.id])

        if len(obj_idList) < 60:
            return obj_idList
        else:
            return obj_idList[:60]

    # HOG descriptor를 추출하는 함수
    @staticmethod
    def createHOGinfo(imageFile):
        image = pil.open(imageFile)
        image = np.asarray(image)
        image = color.rgb2gray(image)
        image = cv2.resize(image, (256, 256))
        fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1),
                            block_norm="L2-Hys",
                            visualise=True)
        fd = np.float32(fd)
        return fd

    @staticmethod
    def getImageLabelByCNN(image):
        answer = run_inference_on_image(BASE_DIR + "/" + str(image.imageFile))
        print (answer)

    # 라벨로 이미지를 검색하는 함수
    @staticmethod
    def getImageListBySearch(label, searchText):
        images = Image.objects.filter(Q(label__contains=label) | Q(title__contains=searchText))
        return images.order_by('-created')