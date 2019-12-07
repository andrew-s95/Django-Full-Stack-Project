from __future__ import unicode_literals
from django.db import models
import re

# email validation - standard email format
e_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# password validation - minimum 8 char, have 1 number, 1 lowercase, 1 uppercase
pw_regex = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}')

class LoginManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 1 or len(postData["lname"]) < 1:
            errors["name"] = "Names have to be more than initials."
        if not e_regex.match(postData["email"]):
            errors["email"] = "Invalid email address."
        if not pw_regex.match(postData["confirm_pw"]):
            errors["confirm_pw"] = "Passwords must be minimum of 8 char, 1 number, 1 lowercase, and 1 uppercase"
        if postData["pw"] != postData["confirm_pw"]:
            errors["pw_match"] = "Passwords do not match!"
        if User.objects.filter(email = postData['email']):
            errors['email'] = "email is registered"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if not user:
            errors['email'] = "email isn't registered"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

class Comment(models.Model):
    message = models.ForeignKey(Message, related_name="comments")
    user = models.ForeignKey(User, related_name="comments")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

# Create your models here.
