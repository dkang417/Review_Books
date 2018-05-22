# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import bcrypt

class UserManager(models.Manager):
    def validate(self, request):
        if request.method == "POST":
            valid = True
            for key in request.POST:
                if request.POST[key] == "":
                    valid = False
                    messages.error(request, "{} is required".format(key))
            if len(request.POST["password"]) <= 8:
            	valid= False 
            	messages.error(request, "password must be more than 8 characters")
            if request.POST["password"] != request.POST["confirm_password"]:
                valid = False
                messages.error(request, "password must match confirm password")
            if valid:
            	name = request.POST["name"]
            	email = request.POST["email"]
            	password = request.POST["password"]
            	hashed_pw = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

                self.create(name=name, email=email, password=hashed_pw)
                messages.success(request, "Successfully registered")
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class AuthorManager(models.Manager):
	def validate_author(self,request):
		errors= {}
		return errors

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
class BookManager(models.Manager):
	def validate_book(self,request):
		errors= {}
		return errors
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
		return "<Book object: {} {}>".format(self.title,self.author)


class ReviewManager(models.Manager):
	def validate_review(self,request):
		errors= {}
		return errors
		
class Review(models.Model):
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


