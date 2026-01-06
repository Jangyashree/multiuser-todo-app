from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import TODOO
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='/login')
def home(request):
    return render(request, 'signup.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        email = request.POST.get('emailid')
        password = request.POST.get('pwd')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')
    
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('fnm')
        password=request.POST.get('pwd')
        user=authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request,user)
            messages.success(request, "Logged in successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')   
    return render(request, 'login.html')


@login_required(login_url='/login')
def dashboard(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        obj=TODOO(title=title,user=request.user)
        obj.save()
        return redirect('/dashboard')
        
    res=TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard.html',{'res':res})


@login_required(login_url='/login')
def edit_task(request, id):
    obj = get_object_or_404(TODOO, id = id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        obj.title = title
        obj.save()
        return redirect('dashboard')
    
    return render(request, 'edit_task.html', {'obj': obj})


@login_required(login_url='/login')
def delete_task(request, id):
    obj = TODOO.objects.get(id=id, user=request.user)
    obj.delete()
    return redirect('dashboard')


def signout(request):
    logout(request)
    return redirect('/login')