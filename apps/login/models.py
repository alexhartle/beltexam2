from __future__ import unicode_literals
import re, bcrypt
from django.db import models
from django.contrib import messages

# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        duplicate = User.objects.filter(email=postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        DATE_REGEX = re.compile(r'^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/(19|20)\d{2}$')
        if duplicate:
            errors.append("Duplicate user found.")
        if len(postData['first_name']) < 3 or len(postData['last_name']) < 3:
            errors.append("First and last name must be 2 or more characters.")
        if len(postData['email']) == 0:
            errors.append("Email address required.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email address.")
        if not DATE_REGEX.match(postData['date']):
            errors.append("Invalid hiring date.")
        if len(postData['password']) < 8:
            errors.append("Password must be more than 8 characters")
        if postData['password'] != postData['password_conf']:
            errors.append("Passwords did not match.")
        if len(errors) > 0:
            print "Validation failed."
        return errors

    def add_user(self, postData):
        hashedpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=postData['first_name'],
                            last_name=postData['last_name'],
                            email=postData['email'],
                            password=hashedpw)
        user = User.objects.filter(email=postData['email']).first()

    def login(self, postData):
        user = User.objects.filter(email=postData['email'])
        if user:
            user = User.objects.get(email=postData['email'])
            pwhash = user.password.encode()
            if user not in User.objects.all():
                return False
            if pwhash == bcrypt.hashpw(postData['password'].encode(), pwhash):
                return True
            elif pwhash is not bcrypt.hashpw(postData['password'].encode(), pwhash):
                return False
        return False

### DEAR SELF: PLEASE DON'T FORGET! ###
### TO LINK TO THIS TABLE AND ACROSS APPS CREATE A ###
### FOREIGN KEY IN THE NEXT APP REFERENCING THIS TABLE ###
### DONT FORGET TO IMPORT THE LINKED MODEL FROM .MODELS ###
### YOU CAN THEN CALL VALUES FROM THIS TABLE SIMPLY BY ###
### SAYING User.<desired table> AS THE ORM CREATES THEM ###
### FOR YOU! COOL STUFF MAN ###
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
