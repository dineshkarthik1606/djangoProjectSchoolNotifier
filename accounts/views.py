from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('home')
        else:
            print("invalid creds")
            messages.info(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logut(request):
    auth.logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Passwords not matching")
            return redirect('signup')
        

    else:
        return render(request, 'signup.html')
