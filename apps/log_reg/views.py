from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    
    return render(request,'log_reg/index.html')

def success(request):
    if not "logged_id" in request.session:
        return redirect("/log_reg")
    data = {
        "loggeduser": User.objects.get(id=request.session["logged_id"])
    }
    
    return render(request,'log_reg/success.html', data)

def login(request):
    if request.method == 'POST':
        checklogin = User.objects.login_validator(request.POST)
        if "user" in checklogin:
            request.session["logged_id"] = checklogin["user"].id
            request.session["idk"] = "logged in"
            return redirect('/log_reg/success')
        else:
            for tag, error in checklogin.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/log_reg')
        
    else:
        return redirect("/log_reg")


def registration(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if "user" in errors: 
            request.session["idk"] = "registered"
            request.session["logged_id"] = errors["user"].id
            return redirect('/log_reg/success')

        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/log_reg')
    else:
        return redirect("/log_reg")

def logout(request):
    request.session.clear()
    return redirect("/log_reg")
    

            
            