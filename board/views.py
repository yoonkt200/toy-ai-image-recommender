import time
import os
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect

from processor.models import Image


@csrf_exempt
def Board(request):
    images = Image.objects.all()
    return render(request, 'pages/board/board.html', {'images': images})


@csrf_exempt
def GetImage(request):
    files = request.FILES['file']
    title = request.FILES['file'].name
    Image.createImage(title, files)

    return JsonResponse({'result': 'success'})