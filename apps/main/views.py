from django.shortcuts import render, redirect
import time
from .models import User, Appointments
from django.contrib import messages

# Create your views here.
def index(request):
    if "id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')
    today = time.strftime("%Y-%m-%d")
    dateNice = time.strftime("%m-%d-%Y")
    user = User.objects.get(id=request.session['id'])
    todaysAppointments = Appointments.objects.filter(user=user, date=today).order_by('date', 'time')
    allUserAppointments = Appointments.objects.filter(user=user).exclude(id__in=todaysAppointments).order_by('date', 'time')
    context = { 'today': today,
                'dateNice': dateNice,
                'allUserAppointments': allUserAppointments,
                'todaysAppointments': todaysAppointments }
    return render(request, "main/index.html", context)

def add(request):
    errors = Appointments.objects.validate(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/main')
    user = User.objects.get(id=request.session['id'])
    Appointments.objects.create(task = request.POST['task'],
                                date = request.POST['date'],
                                time = request.POST['time'],
                                user = user)
    return redirect('/main')

def edit(request, id):
    appointment = Appointments.objects.get(id=id)
    context = { "appointment" : appointment }
    return render(request,'main/edit.html', context)

def editAppointment(request, id):
    errors = Appointments.objects.validate(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/main/edit/'+id)
    Appointments.objects.filter(id=id).update(task = request.POST['task'],
                       date = request.POST['date'],
                       time = request.POST['time'],
                       status = request.POST['status'])
    return redirect('/main')

def delete(request, id):
    Appointments.objects.filter(id=id).delete()
    return redirect('/main')

def logout(request):
    request.session.flush()
    return redirect('/')
