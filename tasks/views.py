from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):

  print(request.POST)
  return render(request, 'signup.html', {
    'form':UserCreationForm
  })

