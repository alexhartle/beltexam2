from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    context = { 'users': User.objects.all() }
    return render(request, 'login/index.html', context)

def register(request):
    errors = User.objects.register(request.POST)
    print errors
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    User.objects.add_user(request.POST)
    messages.success(request, "User succesfully created. Please log in.")
    return redirect('/')

def login(request):
    status = User.objects.login(request.POST)
    if status is True:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['full_name'] = user.first_name + " " + user.last_name
        request.session['email'] = user.email
        ### THIS IS WHERE THE NEXT ROUTE GOES ONCE LOGGED IN ###
        return redirect('/main/')
    if status is False:
        print status
        messages.error(request, "Username or password incorrect.")
        return redirect('/')
