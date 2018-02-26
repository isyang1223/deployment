from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import * 

def index(request):
    context = {
        "course": Course.objects.all()
    }
    return render(request,'courses_app/index.html', context)

def add(request):
    if request.method == "POST":
        errors = Course.objects.basic_validator(request.POST)
        if len(errors): 
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:

            Course.objects.create(name=request.POST['name'], desc=request.POST['desc'])
    


            return redirect('/')
    
    return redirect('/')

def destroy(request, id):
    removecontext={
        "rcourse": Course.objects.get(id=id)
    }
   
    return render(request,'courses_app/destroy.html', removecontext) 

def go_back(request):

    return redirect("/")
    
    
    
def remove(request, id):
    d=Course.objects.get(id=id)
    d.delete()
   
    return redirect("/")
    
   