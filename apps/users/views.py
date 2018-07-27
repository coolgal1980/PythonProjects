from django.shortcuts import render, redirect, reverse
from .models import User
from django.contrib import messages

def index(request):  
    if 'first_name' not in request.session:
        return render(request, 'users/index.html') 
    else:        
        return redirect('/books/home')       

def create(request):
    result = User.objects.reg_validation(request)
    if result[0] == False:
        for error in result[1]:
            messages.error(request, error)
        return redirect('users:index')  
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['first_name'] = user.first_name
        request.session['user_id'] = user.id
        return redirect('/books/home')        

def login(request):    
    result = User.objects.login_validation(request)
    if result[0] == False:
        for error in result[1]:
            messages.error(request, error)
        return redirect('users:index')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['first_name'] = user.first_name
        request.session['email'] = user.last_name
        request.session['user_id'] = user.id
        return redirect('/books/home')
      
def logout(request):
    # request.session.pop('user')
    request.session.clear()
    return redirect('/users')
