from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    
    return render(request,'log_reg/index.html')

def success(request):
    if not "logged_id" in request.session:
        return redirect("/log_reg")
    loginuser = User.objects.get(id= request.session['logged_id'])
    key= Wishlist.objects.filter(added_by=request.session["logged_id"])
    key2= Wishlist.objects.all().exclude(added_by=loginuser).exclude(repeated_by=loginuser)
    key4=Wishlist.objects.all().filter(repeated_by=loginuser)
    data = {
        "loggeduser": loginuser,
        "myallitem":key,
        "notmyitem":key2,
        "myitems":key4,
        
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
def delete(request, id):
    if not "logged_id" in request.session:
        return redirect("/")
    Wishlist.objects.get(id=id).delete()
  
    return redirect('/log_reg/success')

def additem(request):
    if not "logged_id" in request.session:
        return redirect("/")
  
    return render(request,'log_reg/additem.html')

def createitem(request):
    if not "logged_id" in request.session:
        return redirect("/")
    if request.method == 'POST':
        errors = Wishlist.objects.item_validator(request.POST)
        if "exist" in errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/log_reg/additem')
        if "itemname" in errors:
            return redirect("/log_reg/success")

def showitem(request,id):
    if not "logged_id" in request.session:
        return redirect("/")
    key= Wishlist.objects.get(id=id)
    key1=key.repeated_by.all()
    data={
        "item": key,
        "usersitem": key1
    }
    
    return render(request,'log_reg/item.html', data)

def removeitem(request,id):
    user = User.objects.get(id=request.session['logged_id'])
    
    removeitem = Wishlist.objects.get(id=id)
    removeitem.repeated_by.remove(user)
    removeitem.save()
  
    return redirect('/log_reg/success')

def logout(request):
    request.session.clear()
    return redirect("/log_reg")

def addtowishlist(request,id):

    user = User.objects.get(id=request.session['logged_id'])
    
    additem = Wishlist.objects.get(id=id)
    additem.repeated_by.add(user)
    additem.save()
    
    return redirect('/log_reg/success')
    

            
            