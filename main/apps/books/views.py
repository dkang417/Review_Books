from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    if "active_id" in request.session:
        return redirect('/books')
    return render(request, "books/index.html")

def register(request):
    User.objects.validate(request)
    return redirect("/")

def login(request):
    users = User.objects.filter(email=request.POST["email"])
    if len(users) > 0:
        user = users[0]
        password = request.POST['password']
        newPassword = bcrypt.checkpw(password.encode(), user.password.encode())
        if newPassword: 
            request.session["active_id"] = user.id 
            return redirect('/books')
         
    messages.error(request, "Invalid login information")
    return redirect("/")

def books(request):
	#make sure user is logged in
	if request.session.get('active_id') == None:
		return redirect('/')

	
	latest_three = Review.objects.all().order_by('-created_at')[0:3]
	ids = []
	for review in latest_three:
		ids.append(review.book.id)

	context = {
		'user' : User.objects.get(id=request.session['active_id']),
		'latest_three': latest_three,
		'other_books':Book.objects.exclude(id__in=ids),
		
	}
	return render(request, 'books/books.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')

def add(request):
	context = {
		'authors': Author.objects.all()
	}
	return render(request, 'books/add.html', context)

def addbook(request):
	if request.method == "POST":
		
   		author_name = request.POST["new_author"]
   		if author_name == "":
   			author_name = request.POST["old_author"]
   		author = Author.objects.filter(name=author_name)
   		if len(author) == 0:
   			author = Author.objects.create(name = author_name)
   		else: 
   			author = author[0]

		title = request.POST['title']
		review = request.POST['content']
		rating = request.POST['rating']

		book =Book.objects.filter(title=title)
		#check if there is a book with that title
		if len(book) == 0:
			book = Book.objects.create(title=title, author = author)
		else:
			book = book[0]

		#create review	
		Review.objects.create(rating=rating, content = review, user=User.objects.get(id=request.session['active_id']), book = book)

		return redirect("/books/{}".format(book.id))
	else:
		return redirect('/')
def showbook(request, id):
	book = Book.objects.get(id=id)
	reviews = Review.objects.filter(book=book)
	context = {
		'book': book,
		'reviews': reviews
	}

	return render(request, 'books/showbook.html', context)
def getuser(request):

	return redirect("/users/{}".format(user.id))

def showusers(request, id):
	user = User.objects.get(id=id)
	total_reviews= len(user.reviews.all())	
	reviewed_books = Review.objects.filter(user=user)
	

	context = {
		'user': user,
		'total_reviews': total_reviews,
		'reviewed_books': reviewed_books
	}
	return render( request, 'books/showusers.html', context)

def addreview(request,id):
	user = User.objects.get(id=request.session['active_id'])
	book = Book.objects.get(id=id)
	review = request.POST['review']
	rating = request.POST['rating']

	Review.objects.create(rating=rating, content = review, user=user, book = book)
	
	return redirect('/books/{}'.format(book.id))
 
def delete(request,bookid,reviewid):
	review = Review.objects.get(id=reviewid)
	review.delete()
	return redirect('/books/{}'.format(bookid))

