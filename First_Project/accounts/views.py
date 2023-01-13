from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect("list")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, "accounts/register.html", {'form': form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("list")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    return render(request, "accounts/login.html", {'form': form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("list")
