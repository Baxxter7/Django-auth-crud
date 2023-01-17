from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task

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
    #datecomplated__isnull es para mostrar solo las que faltan por completar
    #tasks = Task.objects.filter(user = request.user, datecompleted__isnull = True)
    tasks = Task.objects.filter(user = request.user)
    return render(request, 'tasks.html',{
        'tasks': tasks
    })

def task_detail(request, task_id):
    if request.method == "GET":
        #Esta consulta valida que solo podamos visualizar las del usuario logeado
        get_task = get_object_or_404(Task, id = task_id, user = request.user)
        form =TaskForm(instance=get_task)
        return render(request, 'task_detail.html', {
            'task': get_task, 
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, id = task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except:

            return render(request, 'task_detail.html', {
                'form': form,
                'error': 'Error Upating task'
            })
        

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
