from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth  import login

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
                create_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                create_user.save()
                login(request, create_user)
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
