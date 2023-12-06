from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import User,Inventory,Category
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
    if 'category_id' in request.session:
        items = Category.objects.get(id = request.session['category_id']).items.all()
        print(items)
    else:
        items = Inventory.objects.all()
    current_user = User.objects.get(id  =request.session['login_id'])
    categories = Category.objects.all()
    content = {
        'current_user': current_user,
        'items' : items,
        'categories':categories,
    }
    return render(request,'items.html',content)

def add_item_form(request):
    return render(request,'edit_item')

def filter(request):
    request.session['category_id'] = request.POST['filter']
    return redirect('/dashboard')