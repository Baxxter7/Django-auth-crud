from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
                return HttpResponse('<h1>User created successfully</h1>')
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
