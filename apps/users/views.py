from django.shortcuts import render, redirect, reverse
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):  
    if 'first_name' not in request.session:
        return render(request, 'users/index.html') 
    else:
        return render(request, 'books/home.html')

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
        return redirect(reverse('books:home'))
    # return login_success(request, result[1])

def login(request):
    print ("loginh")
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
        return redirect(reverse('books:home'))
    # return login_success(request, result[1])

# def login_success(request, user):
#     print ("successful login")
#     request.session['user'] = {
#         'id' : user.id,
#         'first_name' : user.first_name,
#         'last_name' : user.last_name,
#         'email' : user.email,
#     }
#     return redirect ('/login/success')


def success(request):
    # if not 'user' in request.session:
    #     return redirect('/login')
    # return render(request, 'login/success.html')
    return render(request, 'books/home.html')

def logout(request):
    # request.session.pop('user')
    request.session.clear()
    return redirect('/users')
