import time

from PIL import Image
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from .utils import process_image


# Create your views here.

def home_page_view(request):
    current_session_user = []
    get_current_user = CurrentUser.objects.all()
    context = {
        'current_session_user': current_session_user,
    }
    for i in get_current_user:
        current_session_user.append(i)
    if request.method == 'POST':
        CurrentUser.objects.all().delete()
        CurrentUser.objects.create(current_user='Вход не выполнен')
        return render(request, 'detector_template/log_out.html', context)
    return render(request, 'detector_template/home_page.html', context)


def object_detector_page_view(request):
    current_session_user = []
    get_current_user = CurrentUser.objects.all()
    context = {
        'current_session_user': current_session_user,
    }
    for i in get_current_user:
        current_session_user.append(i)
        for j in current_session_user:
            if j.current_user == 'Вход не выполнен':
                return render(request, 'detector_template/not_authorized.html', context)
    return render(request, 'detector_template/object_detector_page.html', context)


def register_page_view(request):
    passwords_error = 'Пароли не совпадают'
    user_error = 'Пользователь уже существует'
    current_session_user = []
    get_current_user = CurrentUser.objects.all()
    for i in get_current_user:
        current_session_user.append(i)
    context = {
        'passwords_error': passwords_error,
        'user_error': user_error,
        'current_session_user': current_session_user,
    }
    if request.method == 'GET':
        for j in current_session_user:
            if j.current_user != 'Вход не выполнен':
                return render(request, 'detector_template/already_authorized.html', context)
    get_users = MyAppUser.objects.all()
    users_names = []
    for i in get_users:
        users_names.append(i.name)
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            if password == repeat_password and username not in users_names:
                MyAppUser.objects.create(name=username, user_password=password)
                CurrentUser.objects.all().delete()
                CurrentUser.objects.create(current_user=username)
                for i in get_current_user:
                    current_session_user.append(i)
                return render(request, 'detector_template/valid_registration_page.html', context)
            elif password != repeat_password:
                return render(request, 'detector_template/invalid_password_registration_page.html', context)
            elif username in users_names:
                return render(request, 'detector_template/invalid_user_registration_page.html', context)
    return render(request, 'detector_template/register_page.html', context)


def login_page_view(request):
    passwords_error = 'Пароль не подходит'
    user_error = 'Пользователя не существует'
    current_session_user = []
    get_current_user = CurrentUser.objects.all()
    for i in get_current_user:
        current_session_user.append(i)
    context = {
        'passwords_error': passwords_error,
        'user_error': user_error,
        'current_session_user': current_session_user,
    }
    if request.method == 'GET':
        for j in current_session_user:
            if j.current_user != 'Вход не выполнен':
                return render(request, 'detector_template/already_authorized.html', context)
    get_all_users = MyAppUser.objects.all()
    existed_users_list = []
    for i in get_all_users:
        existed_users_list.append({i.name: i.user_password})
    if request.method == 'GET':
        form = UserSearch(request.GET)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            check_user = {username: password}
            if check_user in existed_users_list:
                CurrentUser.objects.all().delete()
                CurrentUser.objects.create(current_user=username)
                for i in get_current_user:
                    current_session_user.append(i)
                return render(request, 'detector_template/successful_authorization_page.html', context)
            else:
                return render(request, 'detector_template/user_not_found_page.html', context)
    return render(request, 'detector_template/login_page.html', context)



def display_myapp_images(request):
    name_for_display = None
    current_session_user = []
    get_current_user = CurrentUser.objects.all()
    for i in get_current_user:
        current_session_user.append(i.current_user)
    for j in current_session_user:
        if name_for_display is None:
            name_for_display = j
    if request.method == 'GET':
        get_current_user_pics = UserImage.objects.filter(enter_user_name=name_for_display)
        return render(request, 'detector_template/display_myapp_images.html',
                      {
                          'get_current_user_pics': get_current_user_pics,
                          'current_session_user': current_session_user,
                      })
    if request.method == 'POST':
        get_current_user_pics = UserImage.objects.filter(enter_user_name=name_for_display)
        delete_images = UserImage.objects.filter(enter_user_name=name_for_display)
        delete_images.delete()
        return render(request, 'detector_template/object_detector_page.html',
                      {
                          'get_current_user_pics': get_current_user_pics,
                          'current_session_user': current_session_user,
                      })


def process_image_feed(request):
    name_for_display = None
    current_session_user = []
    get_current_user = CurrentUser.objects.all()
    for i in get_current_user:
        current_session_user.append(i.current_user)
    for j in current_session_user:
        if name_for_display is None:
            name_for_display = j
    if request.method == 'GET':
        get_processed = ProcessedUserImage.objects.filter(image_user_name=name_for_display)
        return render(request, 'detector_template/display_processed_images.html',
                      {
                          'current_session_user': current_session_user,
                          'get_processed': get_processed,
                      })
    if request.method == 'POST':
        get_current_user_pics = ProcessedUserImage.objects.filter(image_user_name=name_for_display)
        delete_images = ProcessedUserImage.objects.filter(image_user_name=name_for_display)
        delete_images.delete()
        return render(request, 'detector_template/object_detector_page.html',
                      {
                          'get_current_user_pics': get_current_user_pics,
                          'current_session_user': current_session_user,
                      })
    return render(request, 'detector_template/display_processed_images.html')


def pic_load_page_view(request):
    name_for_display = None
    current_session_user = []
    get_current_user = CurrentUser.objects.all()
    for i in get_current_user:
        current_session_user.append(i.current_user)
    for j in current_session_user:
        if name_for_display is None:
            name_for_display = j
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            process_image(name_for_display)
            UserImage.objects.filter(enter_user_name=name_for_display, was_processed=False).update(was_processed=True)
            return HttpResponseRedirect("/object_detector_page")
    else:
        form = ImageUploadForm()
    return render(request, 'detector_template/pic_load_page.html', {
        'form': form,
        'current_session_user': current_session_user,
    })
