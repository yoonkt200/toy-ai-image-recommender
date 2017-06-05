# -*- coding: utf-8 -*-

import time
import os
import json
import cv2

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from processor.models import Image


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
    Image.createImage(title, files)

    return JsonResponse({'result': 'success'})