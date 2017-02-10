from django.shortcuts import *
from django.http import *
from .models import User
from django.core.mail import *
from random import *


def home_page(request):
    return render(request, "Chess/home.html")


def login_page(request):
    return render(request, "Chess/login.html")


def signup_page(request):
    return render(request, "Chess/signup.html")


def info_signup(request):
    same = User.objects.filter(username=request.POST['username'])
    if (not same):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        key = randint(1000, 9999)
        user = User(username = username, email = email, password = password, activation_key = key, activation_status = 0)
        user.save()
        # return HttpResponse (user)
        send_mail(
            'Activation key',
            'Hello dear' + str(username) + 'Here is your activation key:' + str(key),
            'mypythonaichess@gmail.com',
            [user.email],
            fail_silently=False,
        )
        context = {'user': user}
        return render(request, 'Chess/login.html', context)
    else:
        error = "This username has been taken already !"
        context = {'error': error}
        return render(request, 'Chess/signup.html', context)


def info_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.filter(username = username)

    if (user):
        user_1 = User.objects.get(username = username, password = password)
        if (user_1.activation_status == 0):
            return render(request, 'Chess/activation.html')
        else:
            context = {'user': user_1}
            return render(request, 'Chess/info.html', context)
    else:
        error = "Wrong Username Or Password !"
        context = {'error': error}
        return render(request, 'Chess/login.html', context)


def activation(request):
    user = User.objects.get(username = request.POST['username'])
    activation_key = request.POST['activation_key']
    activation_key = int(activation_key)

    if (int(user.activation_key) == activation_key):
        tmpuser = user
        user.delete()
        tmpuser.activation_status = 1
        tmpuser.save()
        context = {'user' : user}
        return render(request, 'Chess/info.html', context)
    else:
        error = "WRONG CODE !!"
        context = {'error' : error}
        return render(request, 'Chess/activation.html', context)
