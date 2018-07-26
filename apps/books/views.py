from django.shortcuts import render, redirect

from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *


# Create your views here.
def home(request):    
    if not 'first_name' in request.session:
        return redirect('users:index')        
    else:
        reviews = Review.objects.all().order_by('-id')[:3]
        books = Book.objects.all()
        context = {
            'reviews':reviews,
            'books':books
        }
        return render(request, 'books/home.html', context)

def add_book(request):
    if not 'first_name' in request.session:
        return redirect('users:index')
    else:
        if request.method == 'POST':
            author=''
            if len(request.POST['author2'])<1:
                if not Book.objects.filter(author=request.POST['author1']):
                    messages.warning(request, "Please select or add author")
                if Book.objects.get(author=request.POST['author1']):
                    author=request.POST['author1']

            if len(request.POST['author2'])>1:
                author=request.POST['author2']

            if not Book.objects.filter(book_title=request.POST['book_title'], author=author):
                Book.objects.create(book_title=request.POST['book_title'], author=author)
                book = Book.objects.get(book_title=request.POST['book_title'], author=author)
                book.book_reviews.create(review=request.POST['review'], rating = request.POST['rating'], user_id=request.session['user_id'])
                return redirect(reverse('books:show', kwargs={'id':book.id}))

        books=Book.objects.all()
        context={
            'books': books
        }

        return render(request, 'books/add_book.html', context)

def show(request, id):
    if not 'first_name' in request.session:
        return redirect('users:index')
    else:
        book = Book.objects.get(id=id)
        reviews = book.book_reviews.all()
        context = {
            'book': book,
            'reviews':reviews
        }
        return render(request, 'books/book_reviews.html', context)

def create_review(request, id):
    if not 'first_name' in request.session:
        return redirect('users:index')
    else:
        Review.objects.create(review=request.POST['new_review'], rating=request.POST['rating'], book_id=id, user_id=request.session['user_id'])
        # return redirect(reverse('books:show', kwargs={'id':id}))
        return redirect('books:show', kwargs={'id':id})

def destroy(request, id):
    if not 'first_name' in request.session:
        return redirect('users:index')
    else:
        Review.objects.get(id=id).delete()
        return redirect(reverse('books:home'))

def user(request, id):
    if not 'first_name' in request.session:
        return redirect('users:index')
    else:
        user = User.objects.get(id=id)
        reviews = user.user_reviews.all()
        total = len(reviews)
        context = {
            'user':user,
            'reviews':reviews,
            'total':total
        }
        return render(request, 'books/user_reviews.html', context)
