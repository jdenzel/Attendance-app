from django.shortcuts import render, redirect
from attendance.forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import TimeClock
from django.utils import timezone

# Create your views here.
@login_required(login_url="/login")
def home(request):
    return render(request, 'attendance/home.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): # Checks if all form fields is correct
            user = form.save() # Creates new user and saves into database then assigns it to user variable
            login(request, user) # Logs in newly created user
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
def clock_in(request):
    if request.method == 'POST':
        time_clock = TimeClock(employee=request.user, role=request.POST.get('role')) # Creates a new TimeClock instance and requests the desired role of the currently logged in user
        time_clock.save() # Saves the Instance
        request.session['clocked_in'] = True # Sets clocked_in variable to True to tell indicate the user is clocked in
        return redirect('clock_out') # Changes view to clock out view
    return render(request, 'attendance/clock_in.html') # Renders clock in view if method is not POST

@login_required(login_url="/login")
def clock_out(request):
    time_clock = TimeClock.objects.filter(employee=request.user).latest('clock_in_time') # Retrieves the latest TimeClock instance
    if request.method == 'POST':
        time_clock.clock_out_time = timezone.now() # Sets the clock_out_time to the current time
        time_clock.save() # Saves the Instance
        request.session['clocked_in'] = False # Sets clocked_in to False to indicate user is clocked out
        return redirect('clock_in') # Changes view to clocked_in view
    return render(request, 'attendance/clock_out.html', {'time_clock': time_clock}) # Renders clocked out view if method is not POST
    # {'time_clock': time_clock} This passes the time_clock to the template