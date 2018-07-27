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
            # if not Book.objects.filter(author=request.POST['author1']):
            #     messages.error(request, "Please select or add author")
            # if Book.objects.get(author=request.POST['author1']):
            #     author=request.POST['author1']
            print("authoris",  request.POST['author1'])
            print("lenauthr2", len(request.POST['author2']))
            if len(request.POST['author1']) < 1 or request.POST['author1'] == '' or request.POST['author1'] == '0':
                print("insidefirstif")
                if len(request.POST['author2'])<1:
                    print("second if")
                    messages.error(request, "Please select or add author") 
                    return redirect('books:add_book')  
                    # return render(request, 'books/add_book.html')                          
                else:
                    author=request.POST['author2'] 
            else:
                author=request.POST['author1'] 
                # try:
                #     print("intryblock")
                #     Book.objects.filter(author=request.POST['author2'])
                #     messages.error(request, "This author exists in DB. Please select or add new")   
                #     return render(request, 'books/add_book.html', context)                                 
                # except:     
                #     author=request.POST['author1'] 

            # if len(request.POST['author2'])>1:
            #     author=request.POST['author2']

            if not Book.objects.filter(book_title=request.POST['book_title'], author=author):
                Book.objects.create(book_title=request.POST['book_title'], author=author)
                book = Book.objects.get(book_title=request.POST['book_title'], author=author)
                book.book_reviews.create(review=request.POST['review'], rating = request.POST['rating'], user_id=request.session['user_id'])
                storage = messages.get_messages(request)
                for _ in storage: 
                    pass

                if len(storage._loaded_messages) == 1: 
                    del storage._loaded_messages[0]
                # return redirect(reverse('books:show', kwargs={'id':book.id})) 
                return redirect('books:show', id=book.id)

                # -- This is not rite -- 
                # return redirect('books:show', args={'id':book.id})  
                # NoReverseMatch at /books/add_book/
                # Reverse for 'show' with keyword arguments '{'args': {'id': 19}}' not found. 
                # 1 pattern(s) tried: [u'books/show/(?P<id>\\d+)$']
                           
                # context  does not work with redirects only with render
                # context={
                #     'id': book.id
                # }
                # return redirect('/books/show/', context)
           

            else:                
                messages.error(request, "Book with that title/author already exists") 
                return redirect('books:add_book')  

        books=Book.objects.all()
        context={
            'books': books
        }
        print("addbook")
        return render(request, 'books/add_book.html', context)

def show(request, id):
    if not 'first_name' in request.session:
        return redirect('users:index')
    else:
        print("in here")
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
        return redirect('books:show', id=id)
        # return redirect('books:show', kwargs={'id':id})

def destroy(request, id):
    if not 'first_name' in request.session:
        return redirect('users:index')
    else:
        Review.objects.get(id=id).delete()
        # return redirect(reverse('books:home'))
        return redirect('books:home')

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
