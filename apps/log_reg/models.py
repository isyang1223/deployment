from __future__ import unicode_literals
from django.db import models
from datetime import datetime  
import re 
import bcrypt
NAME_REGEX = re.compile(r'^[a-zA-Z\s]+$')
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "User's name needs to be at least 3 characters!"
        if len(postData['username']) < 3:
            errors["username"] = "User name needs to be at least 3 characters!"
        if not NAME_REGEX.match(postData['name']):
            errors["name"] = "User's name cannot contain any numbers or special characters!"
        if len(postData['datehired']) == 0:
            errors['datehired'] = "Date hired may not be blank!"
        if len(postData['password']) < 8:
            errors["password"] = "Invalid Username/Password!"
        
        if not postData['password'] == postData['password2']:
            errors["password2"] = "Password is not matching with confirm password!"
        if len(User.objects.filter(username=postData["username"])) > 0:
            errors["username"] = "username already exist"
        if len(errors) == 0:
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=postData['name'], username=postData['username'], password=hash1, hireddate=postData['datehired'] )
            errors['user'] = user
        return errors

    def login_validator(self, postData):
        errors={}
        checklogin= User.objects.filter(username=postData["username"])
        if checklogin:
            if bcrypt.checkpw(postData['password'].encode(), checklogin[0].password.encode()) == True:
                errors["user"]=checklogin[0]
            else:
                errors["errorsuser"]="Login failed"
        else:
            errors["errorsuser"]="Login failed"
        return errors

    def item_validator(self, postData):
        errors={}
        checkitem = Wishlist.objects.filter(itemname=postData["itemname"])

        if checkitem:
            errors["exist"] = "This item already exists"
            return errors
        if len(postData['itemname']) < 3:
            errors["exist"] = "Item's name needs to be at least 3 characters!"
            return errors
        if len(postData['itemname']) < 1:
            errors["exist"] = "Item's name cannot be empty!"
            return errors
        a = Wishlist.objects.create(itemname=postData['itemname'], added_by_id=int(postData['addby_id']))
        errors["itemname"] = a
        return errors


class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    hireddate = models.DateTimeField(default=datetime.now)
    password = models.CharField(max_length = 255, default="")
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Wishlist(models.Model):
    itemname = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    repeated_by = models.ManyToManyField(User, related_name="wishlists")
    added_by = models.ForeignKey(User, related_name='items')
    objects = UserManager()