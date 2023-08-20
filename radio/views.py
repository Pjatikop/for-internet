from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import RadioForm
from .models import Radio
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'radio/home.html')


def signupuser(request):
    if request.method == "GET":
        return render(request, 'radio/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentradios')
            except IntegrityError:
                return render(request, 'radio/signupuser.html', {'form': UserCreationForm(),
                                                                 'error': 'Такое имя пользователя уже существует. Задайте другое имя!'})
        else:
            return render(request, 'radio/signupuser.html', {'form': UserCreationForm(),
                                                             'error': 'Пароли не совпадают!'})


@login_required
def currentradios(request):
    radios = Radio.objects.filter(user=request.user)
    return render(request, 'radio/currentradios.html', {'radios': radios})

@login_required
def logoutuser(request):
    if request.method  == "POST":
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'radio/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'radio/loginuser.html', {'form': AuthenticationForm(),
                                                            'error': 'Неверные данные для входа'})
        else:
            login(request, user)
            return redirect('currentradios')


@login_required
def createradio(request):
    if request.method == "GET":
        return render(request, 'radio/createradio.html', {'form': RadioForm()})
    else:
        try:
            form = RadioForm(request.POST)
            new_radio = form.save(commit=False)
            new_radio.user = request.user
            new_radio.save()
            return redirect('currentradios')
        except ValueError:
            return render(request, 'radio/createradio.html', {'error': 'Переданы неверные данные. Попробуйте еще раз.'})


@login_required
def viewradio(request, radio_pk):
    radio = get_object_or_404(Radio, pk=radio_pk)

    return render(request, 'radio/viewradio.html', {'radio': radio})


@login_required
def deleteradio(request, radio_pk):
    radio = get_object_or_404(Radio, pk=radio_pk, user=request.user)
    if request.method == "POST":
        radio.delete()
        return redirect('currentradios')