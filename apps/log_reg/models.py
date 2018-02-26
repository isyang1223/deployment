from __future__ import unicode_literals
from django.db import models
import re 
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = "User's first name cannot be empty!"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "User's last name cannot be empty!"
        if not NAME_REGEX.match(postData['first_name']):
            errors["first_name"] = "User's first name cannot contain any numbers or special characters!"
        if not NAME_REGEX.match(postData['last_name']):
            errors["last_name"] = "User's last name cannot contain any numbers or special characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email/Password!"
        if len(postData['password']) < 8:
            errors["password"] = "Invalid Email/Password!"
        if not postData['password'] == postData['password2']:
            errors["password2"] = "Password is not matching with confirm password!"
        if len(User.objects.filter(email=postData["email"])) > 0:
            errors["email"] = "Email already exist"
        if len(errors) == 0:
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(fname=postData['first_name'], lname=postData['last_name'], email=postData['email'], password=hash1 )
            errors['user'] = user
        return errors

    def login_validator(self, postData):
        errors={}
        checklogin= User.objects.filter(email=postData["logemail"])
        if checklogin:
            if bcrypt.checkpw(postData['password'].encode(), checklogin[0].password.encode()) == True:
                errors["user"]=checklogin[0]
            else:
                errors["errorsuser"]="Login failed"
        else:
            errors["errorsuser"]="Login failed"
        return errors

class User(models.Model):
    fname = models.CharField(max_length = 255)
    lname = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255, default="")
    created_at = models.DateTimeField(auto_now_add = True)
    


    objects = UserManager()