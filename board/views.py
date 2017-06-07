# -*- coding: utf-8 -*-

import time
import os
import json
import cv2
from skimage.feature import hog
from skimage import data, color, exposure
import numpy as np
from PIL import Image as pil

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from processor.models import Image


def getFirstKey(item):
    return item[0]


def getHOGinfo(imageFile):
    image = pil.open(imageFile)
    image = np.asarray(image)
    image = color.rgb2gray(image)
    image = cv2.resize(image, (256, 256))
    fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), block_norm="L2-Hys",
                        visualise=True)
    fd = np.float32(fd)
    return fd


@csrf_exempt
def Board(request):
    searchText = request.GET.get('search', None)
    if searchText is not None:
        images = Image.getImageListBySearch(searchText)

        # 검색결과 있을때
        if images:
            page_data = Paginator(images, 12)
            page = request.GET.get('page')
        # 검색결과 없을때
        else:
            return render(request, 'pages/board/board_default.html',
                          {'currentPage': 1, 'searchText': searchText})
    else:
        searchText = 'none'
        images = Image.objects.all().order_by('-created')
        page_data = Paginator(images, 12)
        page = request.GET.get('page')

    if page is None:
        page = 1

    try:
        images = page_data.page(page)
    except PageNotAnInteger:
        images = page_data.page(1)
    except EmptyPage:
        images = page_data.page(page_data.num_pages)

    images_page = images

    return render(request, 'pages/board/board.html',
                  {'images': images, 'images_page': images_page, 'currentPage': int(page),
                   'searchText':searchText})


@csrf_exempt
def GetImage(request):
    files = request.FILES['file']
    title = request.FILES['file'].name

    # fd = getHOGinfo(files)
    # result_array = []
    #
    # for i in range(0, 100):
    #     testimage = Image.objects.all().first().imageFile
    #     fd2 = getHOGinfo(testimage)
    #     hog_result = [cv2.compareHist(fd, fd2, 0), str(i + 1)]
    #     result_array.append(hog_result)
    #
    # result_array = sorted(result_array, key=getFirstKey)
    # for x in result_array:
    #     print (x)

    Image.createImage(title, files)

    return JsonResponse({'result': 'success'})