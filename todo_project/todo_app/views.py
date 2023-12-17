from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'] ,password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signup.html', {'form':UserCreationForm(),'error':'Username exists'})

        else:
            #pass not matching
            return render(request, 'todo/signup.html', {'form':UserCreationForm(),'error':'Passwords did not match'})

def currenttodos(request):
    todos = Todo.objects.filter(owner=request.user)
    return render(request, 'todo/current.html',{'todos':todos})

def createtodos(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.owner = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/create.html', {'form':TodoForm(),'error':'Bad Data'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user == None:
            return render(request, 'todo/login.html', {'form':AuthenticationForm(),'error':"Username and Password didn't match"})
        else:
            login(request, user)
            return redirect('currenttodos')
        
def home(request):
    return render(request, 'todo/home.html')