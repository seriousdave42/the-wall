from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User
from wall.models import Post

def index(request):
    if "user_id" in request.session:
        return redirect('/')
    return render(request, 'login.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        birthdate = request.POST['birthdate'],
        email = request.POST['email'],
        password = pw_hash)
    messages.success(request, "Successfully registered! Please log in")
    return redirect('/login')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, "Email not registered")
        return redirect('/login')
    logged_user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['user_id'] = logged_user.id
        request.session['first_name'] = logged_user.first_name
        return redirect('/')
    else:
        messages.error(request, "Incorrect password!")
        return redirect('/login')

# def success(request):
#     if 'user_id' not in request.session:
#         messages.error(request, "Please log in!")
#         return redirect('/')
#     user = User.objects.get(id = request.session['user_id'])
#     context = {
#         "first_name" : user.first_name
#     }
#     return render(request, '.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
