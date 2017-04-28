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
    #list = Image.objects.all()
    hello = tf.constant('Hello, TensorFlow!')
    sess = tf.Session()
    tensor = str(sess.run(hello))
    return render(request, 'pages/board/board.html', {'tensor': tensor})


@csrf_exempt
def GetImage(request):
    files = request.FILES.getlist('file')
    print (files)

    return HttpResponseRedirect('/board')