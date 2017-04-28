import time
import os
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from processor.models import Image


def Board(request):
    #list = Image.objects.all()
    hello = tf.constant('Hello, TensorFlow!')
    sess = tf.Session()
    tensor = str(sess.run(hello))
    return render(request, 'pages/board/board.html', {'tensor': tensor})