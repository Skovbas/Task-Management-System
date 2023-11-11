from datetime import datetime
from sqlite3 import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
import logging


from .forms import RegistrationForm
from .models import Account, Task, Category, Comment

# Create your views here.
def index(request):
    current_user = request.user
    if request.user.is_authenticated:
        tasks = Task.objects.filter(created_by=current_user)
        if tasks:
            return render(request, "app/home.html",{
                "tasks" : tasks,
                "user" : current_user
            })
    else:
        return render(request, "app/index.html",{})
    
def taskPage(request, id):
    current_user = request.user
    logger = logging.getLogger("app.views/taskPage")
    
    if request.method=="GET":
        if request.user.is_authenticated:
            tasks = Task.objects.filter(pk=id)
            if tasks:
                task = get_object_or_404(Task, pk=id)
                comments = Comment.objects.filter(taskName=task).order_by("creation_date")
                logger.info("successful!")
                return render(request, "app/taskPage.html",{
                    "tasks" : tasks,
                    "user" : current_user,
                    "comments" : comments
                })
        else:
            logger.error("Failed data uploading")
            return render(request, "app/taskPage.html",{})
    elif request.method == "POST":
        comment_text = request.POST["comment"]

        task = get_object_or_404(Task, pk=id)
        
        comment = Comment(
            comments=comment_text,
            taskName=task,
        )
        
        comment.save()

        return HttpResponseRedirect(reverse("taskPage",args=[task.pk] ))
    else:
        logger.error("Failed data uploading")
        return render(request, "app/taskPage.html", {})


def taskCreation(request):
    logger = logging.getLogger("app.views/taskCreation")
    if request.method=="GET":
        p = Task.PRIORITY_CHOICES
        prior = [value[1] for value in p]
        return render(request, "app/taskCreation.html",{
        'priority' : prior,
        })
    else:
        title = request.POST["title"]
        due_date_str = request.POST["due_time"]
        description = request.POST["description"]
        category = request.POST["category"]
        priority = request.POST["priority"].lower()

        # Convert the due_date string to a datetime object
        due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        due_date_aware = timezone.make_aware(due_date)
        
        if Task.objects.filter(title=title):
            logger.error("Login failed. Title")
            return render(request, "app/taskCreation.html",{
                'message' : 'Task with this title already exist!'
            })
        elif due_date_aware <= timezone.now():
            logger.error("Login failed. Date can't not be in the past")
            return render(request, "app/taskCreation.html",{
                'date' : 'Choose correct date!'
            })
        else:
            current_user = request.user
            cat, created = Category.objects.get_or_create(name=category)
            
            task = Task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                created_by=current_user,
                categories=cat
            )
            
            task.save()
            logger.info("successful!")
            
            return HttpResponseRedirect(reverse("index"))
    
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


