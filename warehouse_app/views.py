from django.shortcuts import render,redirect,HttpResponse

def index(request):
    return render(request,'login_reg.html')
