from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request,'login_reg.html')

def login(request):
    if not User.objects.filter(email = request.POST['email']):
        messages.error(request, "Account doesnt exist")
        return redirect('/')
        
    else:
        if bcrypt.checkpw(request.POST['password'].encode(), User.objects.get(email = request.POST['email']).password.encode()):
            request.session['login_id'] = User.objects.get(email = request.POST['email']).id
            return redirect('/dashboard')

        else:
            messages.error(request, "password is not correct")
            return redirect('/')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0 :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'],email = request.POST['email'],password = hash_pass)
        request.session['login_id'] = User.objects.last().id
        messages.success(request, "User created Successfully")
        return redirect('/dashboard')
    
def dashboard(request):
    return render(request,'items.html')