from django.shortcuts import render, redirect
from attendance.forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import TimeClock
from django.utils import timezone
from places.fields import PlacesField

# Create your views here.
@login_required(login_url="/login")
def home(request):
    return render(request, 'attendance/home.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): 
            user = form.save() 
            login(request, user) 
            return redirect('/home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {"form": form})

    # Checks if all form fields is correct
    # Creates new user and saves into database then assigns it to user variable
    # Logs in newly created user

@login_required(login_url="/login")
def clock_in(request):
    if request.session.get('clocked_in', False): 
        return redirect('clock_out') 
    if request.method == 'POST':
        time_clock = TimeClock(employee=request.user, role=request.POST.get('role'), location=request.POST.get('location')) 
        time_clock.save() 
        print(time_clock.location)
        request.session['clocked_in'] = True 
        return redirect('clock_out') 
    return render(request, 'attendance/clock_in.html') 

    # Checks if user is already clocked in
    # Redirects to clock_out view if user is already clocked in
    # Creates a new TimeClock instance and requests the desired role and location of the currently logged in user
    # Saves the Instance
    # Sets clocked_in variable to True to tell indicate the user is clocked in
    # Changes view to clock out view
    # Renders clock in view if method is not POST


@login_required(login_url="/login")
def clock_out(request):
    if not request.session.get('clocked_in', False): 
        return redirect('clock_in') 
    time_clock = TimeClock.objects.filter(employee=request.user).latest('clock_in_time') 
    if request.method == 'POST':
        time_clock.clock_out_time = timezone.now() 
        time_clock.save() 
        request.session['clocked_in'] = False 
        return redirect('clock_in') 
    return render(request, 'attendance/clock_out.html', {'time_clock': time_clock})

    # Checks if user is not clocked in
    # Redirects to clock_in view if user is not clocked in
    # Retrieves the latest TimeClock instance
    # Sets the clock_out_time to the current time
    # Saves the Instance
    # Sets clocked_in to False to indicate user is clocked out
    # Changes view to clocked_in view
    # Renders clocked out view if method is not POST
    # {'time_clock': time_clock} - This passes the time_clock to the template

@login_required(login_url="/login")
def timesheet(request):
    if not request.user.is_staff:
        time_clocks = TimeClock.objects.filter(employee=request.user).order_by('-clock_in_time')
        return render(request, 'attendance/time_sheet.html', {'time_clocks':time_clocks})
    else:
        time_clocks = TimeClock.objects.all().order_by('-clock_in_time')
        return render(request, 'attendance/time_sheet.html', {'time_clocks':time_clocks})
