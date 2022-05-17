import re
import threading
import cv2
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators import gzip
from .models import CBA
from decimal import *
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import face_recognition
from .camera import VideoCamera

def home(request):
    if request.user.is_authenticated:
        redirect("Home")
    return render(request, "index.html")


@ensure_csrf_cookie
def register(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        username = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        if not User.objects.filter(username=username).exists():
            usr = User.objects.create_user(username=username, password=pwd)
            usr.save()
            return JsonResponse({'response': 1})
        else:
            return JsonResponse({'response': -1})
    else:
        return render(request, 'Error.html')


@ensure_csrf_cookie
def signin(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        username = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        usr = authenticate(username=username, password=pwd)
        if usr is None:
            if not User.objects.filter(username=username).exists():
                return JsonResponse({'response': -1})
            else:
                return JsonResponse({'response': -2})
        login(request, usr)
        return JsonResponse({'response': 1})
    else:
        return render(request, 'Error.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@login_required
def welcome(request):
    if request.user.is_superuser:
        return render(request, "admin.html")
    else:
        return render(request, "home.html")
    
@login_required
def live_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")

    

def signout(request):
    logout(request)
    return redirect("login")


@login_required
def add_situations(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        size = int(request.POST.get("size"))
        lat = Decimal(request.POST.get("lat"))
        lng = Decimal(request.POST.get("lng"))
        em_val = int(request.POST.get('em-val'))
        phone = int(request.POST.get("phone"))
        lst = []
        for i in range(size):
            f = request.FILES.get(f"files[{i}]")
            handle_uploaded_file(f)
            lst.append(CBA(user=request.user, latitude=lat, longitude=lng, phoneNumber=phone, emergencyValue=em_val))
        CBA.objects.bulk_create(lst)

        return JsonResponse({})
    else:
        return render(request, 'Error.html')
    
    
    
def handle_uploaded_file(f):
    with open(f'./media/_{f}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def error404(request, exception):
    return render(request, 'Error.html', status=404)