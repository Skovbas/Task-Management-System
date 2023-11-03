from sqlite3 import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging

from .forms import RegistrationForm
from .models import Account

# Create your views here.
def index(request):
    return render(request, "app/index.html")

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def loginview(request):
    if request.method == "POST":
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("app.views")
        
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            logger.info("Login successful!")
            return HttpResponseRedirect(reverse("index"))
        else:
            logger.error("Login failed. Please check your username and password.")
            return render(request, "app/login.html", {
                'message' : "Please check your username and password."
            })
        
    return render(request, "app/login.html")

def signUp(request, *args, **kwargs):
    form = RegistrationForm()
    user = request.user
    
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    
    if request.method=="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("index")
                
    return render(request, "app/register.html", {
        'form' : form,
    })


