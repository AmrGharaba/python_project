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
        cat_id = int(request.session['category_id'])
    else:
        items = Inventory.objects.all()
        cat_id = None
    current_user = User.objects.get(id  =request.session['login_id'])
    categories = Category.objects.all()
    content = {
        'current_user': current_user,
        'items' : items,
        'categories':categories,
        'cat_id': cat_id,
    }
    return render(request,'items.html',content)

def add_item_form(request):
    return render(request,'edit_item')

def filter(request):
    request.session['category_id'] = request.POST['filter']
    return redirect('/dashboard')

def item_view(request, id):
    current_user = User.objects.get(id  =request.session['login_id'])
    item = Inventory.objects.get(id = id)
    categories = Category.objects.exclude(items = item)

    content = {
        'current_user': current_user,
        'item' : item,
        'categories':categories,
    }
    return render(request,'view_items.html',content)
def delete_category_item(request, category_id, item_id):
    item = Inventory.objects.get(id = item_id)
    category = Category.objects.get(id = category_id)
    item.categories.remove(category)
    return redirect(f'/item_view/{item_id}')

def add_category(request,id):
    item = Inventory.objects.get(id = id)
    category = Category.objects.get(id = request.POST['category'])
    item.categories.add(category)
    return redirect(f'/item_view/{id}')