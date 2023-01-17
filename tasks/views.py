from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm

# Create your views here.


def index(request):
    return render(request, 'index.html')


def signup(request):

    if request.method == 'GET':

        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                create_user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                create_user.save()
                login(request, create_user)  # Agregar sesion id
                return redirect('tasks')
            except:
                return render(request, 'signup.html',
                              {'form': UserCreationForm,
                               'error': 'username already exists'
                               })
        else:
            return render(request, 'signup.html',
                          {'form': UserCreationForm,
                           'error': 'Password do not match'
                           })


def tasks(request):
    return render(request, 'tasks.html')


def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Please, provide valida data'
            })
            # create_task = Task()


def signout(request):
    logout(request)
    return redirect('index  ')


def signin(request):
    if request.method == "GET":
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)  # Para guardar la sesion
            return redirect('tasks')
